from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'payment_method', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_balance(self, user, payment_method):
        """Calculate current balance for given payment method (cash or bank)."""
        income = Transaction.objects.filter(
            user=user, type='income', payment_method=payment_method
        ).aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(
            user=user, type='expense', payment_method=payment_method
        ).aggregate(total=Sum('amount'))['total'] or 0
        return income - expense

    def perform_create(self, serializer):
        user = self.request.user
        trans_type = serializer.validated_data.get('type')
        payment_method = serializer.validated_data.get('payment_method')
        amount = serializer.validated_data.get('amount')

        if trans_type == 'expense':
            current_balance = self.get_balance(user, payment_method)
            if current_balance - amount < 0:
                raise ValidationError({
                    'detail': f'Insufficient funds in {payment_method}. Available balance: {current_balance:.2f} TND'
                })
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        period = request.query_params.get('period', 'this_month')
        now = timezone.now().date()

        # Define date ranges based on period
        if period == 'this_month':
            start_date = now.replace(day=1)
            end_date = now
            prev_start = (start_date - timedelta(days=1)).replace(day=1)
            prev_end = start_date - timedelta(days=1)
        elif period == 'last_month':
            start_date = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
            end_date = now.replace(day=1) - timedelta(days=1)
            prev_start = (start_date - timedelta(days=1)).replace(day=1)
            prev_end = start_date - timedelta(days=1)
        elif period == 'last_3':
            start_date = now - timedelta(days=90)
            end_date = now
            prev_start = start_date - timedelta(days=90)
            prev_end = start_date - timedelta(days=1)
        elif period == 'last_6':
            start_date = now - timedelta(days=180)
            end_date = now
            prev_start = start_date - timedelta(days=180)
            prev_end = start_date - timedelta(days=1)
        elif period == 'this_year':
            start_date = now.replace(month=1, day=1)
            end_date = now
            prev_start = start_date.replace(year=start_date.year - 1)
            prev_end = start_date - timedelta(days=1)
        else:
            start_date = now.replace(day=1)
            end_date = now
            prev_start = (start_date - timedelta(days=1)).replace(day=1)
            prev_end = start_date - timedelta(days=1)

        def filter_by_date(queryset, start, end):
            return queryset.filter(date__gte=start, date__lte=end)

        # Current period
        curr_income = filter_by_date(Transaction.objects.filter(user=user, type='income'), start_date, end_date).aggregate(total=Sum('amount'))['total'] or 0
        curr_expense = filter_by_date(Transaction.objects.filter(user=user, type='expense'), start_date, end_date).aggregate(total=Sum('amount'))['total'] or 0
        curr_savings = curr_income - curr_expense

        # Previous period
        prev_income = filter_by_date(Transaction.objects.filter(user=user, type='income'), prev_start, prev_end).aggregate(total=Sum('amount'))['total'] or 0
        prev_expense = filter_by_date(Transaction.objects.filter(user=user, type='expense'), prev_start, prev_end).aggregate(total=Sum('amount'))['total'] or 0

        # Average daily spending
        days_in_period = (end_date - start_date).days + 1
        avg_daily_spending = curr_expense / days_in_period if days_in_period > 0 else 0

        # Largest expense
        largest_expense_qs = filter_by_date(Transaction.objects.filter(user=user, type='expense'), start_date, end_date)
        largest_expense = largest_expense_qs.order_by('-amount').first()
        largest_expense_amount = largest_expense.amount if largest_expense else 0

        # Cash & Bank balances (all time) – non‑negative (display only)
        cash_income = Transaction.objects.filter(user=user, type='income', payment_method='cash').aggregate(total=Sum('amount'))['total'] or 0
        cash_expense = Transaction.objects.filter(user=user, type='expense', payment_method='cash').aggregate(total=Sum('amount'))['total'] or 0
        cash_balance_display = max(float(cash_income - cash_expense), 0.0)

        bank_income = Transaction.objects.filter(user=user, type='income', payment_method='bank').aggregate(total=Sum('amount'))['total'] or 0
        bank_expense = Transaction.objects.filter(user=user, type='expense', payment_method='bank').aggregate(total=Sum('amount'))['total'] or 0
        bank_balance_display = max(float(bank_income - bank_expense), 0.0)

        # Top spending categories (all time)
        top_categories = Transaction.objects.filter(user=user, type='expense').values('category').annotate(total=Sum('amount')).order_by('-total')[:5]
        top_categories_list = [{'category': item['category'] or 'Uncategorized', 'total': round(float(item['total']), 2)} for item in top_categories]

        # Recent 5 transactions
        recent = Transaction.objects.filter(user=user).order_by('-date')[:5]
        recent_serialized = TransactionSerializer(recent, many=True).data

        # Monthly trend – last 6 calendar months
        months_data = []
        today = now
        for i in range(5, -1, -1):
            month_start = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1, day=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1, day=1)
            inc = Transaction.objects.filter(
                user=user, type='income', date__gte=month_start, date__lt=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            exp = Transaction.objects.filter(
                user=user, type='expense', date__gte=month_start, date__lt=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            months_data.append({
                'month': month_start.strftime('%b %Y'),
                'income': round(float(inc), 2),
                'expense': round(float(exp), 2),
                'savings': round(float(inc - exp), 2)
            })

        return Response({
            'cashBalance': round(cash_balance_display, 2),
            'bankBalance': round(bank_balance_display, 2),
            'monthlyIncome': round(float(curr_income), 2),
            'monthlyExpenses': round(float(curr_expense), 2),
            'monthlySavings': round(float(curr_savings), 2),
            'netCashflow': round(float(curr_savings), 2),
            'avgDailySpending': round(avg_daily_spending, 2),
            'largestExpense': round(float(largest_expense_amount), 2),
            'prevMonthIncome': round(float(prev_income), 2),
            'prevMonthExpenses': round(float(prev_expense), 2),
            'topCategories': top_categories_list,
            'recentTransactions': recent_serialized,
            'monthlyTrend': months_data,
        })

    @action(detail=False, methods=['get'], url_path='export')
    def export_csv(self, request):
        """
        Export all user transactions as CSV.
        Access via /api/transactions/export/
        """
        user = request.user
        transactions = self.get_queryset().order_by('-date')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Type', 'Amount', 'Category', 'Description', 'Date', 'Payment Method'])
        for t in transactions:
            writer.writerow([
                t.id,
                t.type,
                t.amount,
                t.category or '',
                t.description or '',
                t.date.isoformat(),
                t.payment_method
            ])
        return response