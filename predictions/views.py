from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
from transactions.models import Transaction
from .models import Goal

class ExpensePredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        end = datetime.now().replace(day=1)
        start = end - timedelta(days=365)
        months = []
        expenses = []
        incomes = []
        for i in range(12):
            month_start = start + timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            total_exp = Transaction.objects.filter(
                user=user, type='expense',
                date__gte=month_start, date__lte=month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            total_inc = Transaction.objects.filter(
                user=user, type='income',
                date__gte=month_start, date__lte=month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            months.append(i+1)
            expenses.append(float(total_exp))
            incomes.append(float(total_inc))

        if len(expenses) < 3:
            return Response({'error': 'Not enough data'})

        X = np.array(months).reshape(-1,1)
        model_exp = LinearRegression()
        model_exp.fit(X, expenses)
        next_month = len(months)+1
        pred_exp = model_exp.predict([[next_month]])[0]

        model_inc = LinearRegression()
        model_inc.fit(X, incomes)
        pred_inc = model_inc.predict([[next_month]])[0]
        pred_savings = pred_inc - pred_exp

        risk = 0.0
        if len(expenses) and pred_exp > expenses[-1] * 1.2:
            risk = (pred_exp - expenses[-1]) / expenses[-1]
            risk = min(risk, 1.0)

        # Anomaly detection
        last_month_start = datetime.now().date() - timedelta(days=30)
        recent_expenses_qs = Transaction.objects.filter(
            user=user, type='expense', date__gte=last_month_start
        ).values_list('amount', flat=True)
        recent_expenses = [float(a) for a in recent_expenses_qs]
        anomalies = []
        if recent_expenses:
            avg = sum(recent_expenses) / len(recent_expenses)
            std = (sum((x - avg)**2 for x in recent_expenses) / len(recent_expenses))**0.5
            threshold = avg + 2*std
            high_exp = [x for x in recent_expenses if x > threshold]
            anomalies = high_exp

        return Response({
            'predicted_expense_next_month': round(pred_exp, 2),
            'predicted_income_next_month': round(pred_inc, 2),
            'predicted_savings_next_month': round(pred_savings, 2),
            'risk_score': round(risk, 2),
            'recommendation': 'Consider reducing discretionary spending' if risk > 0.3 else 'On track',
            'historical_expenses': [round(e, 2) for e in expenses],
            'historical_incomes': [round(i, 2) for i in incomes],
            'anomalies_count': len(anomalies),
            'anomaly_examples': [round(a, 2) for a in anomalies[:3]],
        })

class AIInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now().date()

        # Category trends (month over month)
        categories = Transaction.CATEGORY_CHOICES if hasattr(Transaction, 'CATEGORY_CHOICES') else []
        category_trends = []
        for cat_code, cat_name in categories:
            current_month_start = now.replace(day=1)
            last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
            last_month_end = current_month_start - timedelta(days=1)

            current_spent = Transaction.objects.filter(
                user=user, type='expense', category=cat_code, date__gte=current_month_start
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            previous_spent = Transaction.objects.filter(
                user=user, type='expense', category=cat_code, date__gte=last_month_start, date__lte=last_month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            current_spent = float(current_spent)
            previous_spent = float(previous_spent)

            if previous_spent > 0:
                change = ((current_spent - previous_spent) / previous_spent) * 100
                direction = 'increased' if change > 0 else 'decreased'
                category_trends.append({
                    'category': cat_name,
                    'change_percent': round(abs(change), 1),
                    'direction': direction,
                    'insight': f"{cat_name} spending {direction} {abs(round(change,1))}% compared to last month."
                })
            elif current_spent > 0:
                category_trends.append({
                    'category': cat_name,
                    'change_percent': 100,
                    'direction': 'increased',
                    'insight': f"You started spending on {cat_name} this month."
                })

        # Recurring expenses detection
        recurring = []
        for cat_code, cat_name in categories:
            monthly_spending = []
            for i in range(3):
                month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
                month_end = (month_start + timedelta(days=32)).replace(day=1)
                total = Transaction.objects.filter(
                    user=user, type='expense', category=cat_code, date__gte=month_start, date__lt=month_end
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                monthly_spending.append(float(total))
            if len(monthly_spending) == 3 and all(m > 0 for m in monthly_spending):
                avg = sum(monthly_spending) / 3
                if all(abs(m - avg) / avg <= 0.1 for m in monthly_spending):
                    recurring.append({
                        'category': cat_name,
                        'average_amount': round(avg, 2),
                        'months': 3
                    })

        # Budget recommendations
        total_monthly_expense = Transaction.objects.filter(
            user=user, type='expense', date__gte=now.replace(day=1)
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        total_monthly_expense = float(total_monthly_expense)
        suggested_budget = round(total_monthly_expense * 0.9, 2) if total_monthly_expense > 0 else 0

        # Overspending alerts
        alerts = []
        for cat_code, cat_name in categories:
            avg_spent = Transaction.objects.filter(
                user=user, type='expense', category=cat_code
            ).aggregate(avg=Avg('amount'))['avg'] or 0
            avg_spent = float(avg_spent)
            if avg_spent > 0:
                current_spent = Transaction.objects.filter(
                    user=user, type='expense', category=cat_code, date__gte=now.replace(day=1)
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                current_spent = float(current_spent)
                if current_spent > avg_spent * 1.2:
                    alerts.append(f"⚠️ {cat_name} spending is 20% above your average. Consider cutting back.")

        # Savings forecast
        monthly_savings = []
        for i in range(6):
            month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            inc = Transaction.objects.filter(user=user, type='income', date__gte=month_start, date__lt=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
            exp = Transaction.objects.filter(user=user, type='expense', date__gte=month_start, date__lt=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
            monthly_savings.append(float(inc) - float(exp))
        if len(monthly_savings) >= 3:
            X = np.array(range(len(monthly_savings))).reshape(-1,1)
            y = np.array(monthly_savings)
            model = LinearRegression().fit(X, y)
            next_savings = model.predict([[len(monthly_savings)]])[0]
            savings_forecast = round(next_savings, 2)
        else:
            savings_forecast = 0

        return Response({
            'category_trends': category_trends,
            'recurring_expenses': recurring,
            'budget_recommendation': f"Consider setting a monthly budget of {suggested_budget:.2f} TND based on your spending patterns.",
            'overspending_alerts': alerts,
            'savings_forecast': savings_forecast
        })

class MonthlyReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        now = datetime.now().date()
        last_month_start = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_month_end = now.replace(day=1) - timedelta(days=1)
        total_exp = Transaction.objects.filter(user=user, type='expense', date__gte=last_month_start, date__lte=last_month_end).aggregate(Sum('amount'))['amount__sum'] or 0
        total_inc = Transaction.objects.filter(user=user, type='income', date__gte=last_month_start, date__lte=last_month_end).aggregate(Sum('amount'))['amount__sum'] or 0
        total_exp = float(total_exp)
        total_inc = float(total_inc)
        top_cat = Transaction.objects.filter(user=user, type='expense', date__gte=last_month_start).values('category').annotate(total=Sum('amount')).order_by('-total').first()

        review_text = f"Last month you spent {total_exp:.2f} TND and earned {total_inc:.2f} TND. "
        if top_cat:
            review_text += f"Your top spending category was {top_cat['category']} with {float(top_cat['total']):.2f} TND. "
        if total_inc - total_exp > 0:
            review_text += "You saved money – great job!"
        else:
            review_text += "Your expenses exceeded income. Try to cut back on non-essentials."

        return Response({
            'month': last_month_start.strftime('%B %Y'),
            'total_expense': round(total_exp, 2),
            'total_income': round(total_inc, 2),
            'net_savings': round(total_inc - total_exp, 2),
            'review': review_text
        })

from rest_framework import viewsets
from .models import Goal
from .serializers import GoalSerializer

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)