import math
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
from transactions.models import Transaction

def calculate_health_score(user):
    """Compute financial health score from 0 to 100."""
    incomes = Transaction.objects.filter(user=user, type='income').aggregate(total=Sum('amount'))['total'] or 0
    expenses = Transaction.objects.filter(user=user, type='expense').aggregate(total=Sum('amount'))['total'] or 0
    savings = incomes - expenses
    savings_rate = (savings / incomes * 100) if incomes > 0 else 0

    # Stability: variance in monthly spending over last 6 months
    now = timezone.now().date()
    monthly_spending = []
    for i in range(6):
        start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        total = Transaction.objects.filter(user=user, type='expense', date__gte=start, date__lt=end).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_spending.append(float(total))
    if len(monthly_spending) > 1:
        avg = sum(monthly_spending) / len(monthly_spending)
        variance = sum((x - avg)**2 for x in monthly_spending) / len(monthly_spending)
        stability_score = max(0, 100 - min(100, variance / avg * 10)) if avg > 0 else 100
    else:
        stability_score = 100

    risk_score = min(100, (expenses / incomes * 100)) if incomes > 0 else 100
    budget_score = 80 if savings_rate > 10 else 60 if savings_rate > 0 else 40

    health_score = (savings_rate * 0.3) + (stability_score * 0.3) + (100 - risk_score) * 0.2 + budget_score * 0.2
    return round(health_score, 2)

def get_heatmap_data(user, days=90):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    transactions = Transaction.objects.filter(
        user=user, type='expense', date__gte=start_date, date__lte=end_date
    )
    date_totals = {}
    for t in transactions:
        date_totals[t.date] = date_totals.get(t.date, 0) + float(t.amount)
    result = []
    current = start_date
    while current <= end_date:
        result.append({
            'date': current.isoformat(),
            'value': date_totals.get(current, 0)
        })
        current += timedelta(days=1)
    return result

def get_forecast_data(user, months=6):
    now = timezone.now().date()
    historical_expenses = []
    historical_incomes = []
    months_list = []
    for i in range(12):
        start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        exp = Transaction.objects.filter(user=user, type='expense', date__gte=start, date__lt=end).aggregate(Sum('amount'))['amount__sum'] or 0
        inc = Transaction.objects.filter(user=user, type='income', date__gte=start, date__lt=end).aggregate(Sum('amount'))['amount__sum'] or 0
        historical_expenses.append(float(exp))
        historical_incomes.append(float(inc))
        months_list.append(i+1)

    if len(historical_expenses) >= 3:
        X = np.array(months_list).reshape(-1,1)
        model_exp = LinearRegression().fit(X, historical_expenses)
        model_inc = LinearRegression().fit(X, historical_incomes)
        next_months = [len(months_list)+i+1 for i in range(months)]
        X_pred = np.array(next_months).reshape(-1,1)
        pred_expenses = model_exp.predict(X_pred).tolist()
        pred_incomes = model_inc.predict(X_pred).tolist()
        pred_savings = [pred_incomes[i] - pred_expenses[i] for i in range(months)]
        return {
            'expenses': [round(v,2) for v in pred_expenses],
            'incomes': [round(v,2) for v in pred_incomes],
            'savings': [round(v,2) for v in pred_savings],
        }
    else:
        return {'expenses': [0]*months, 'incomes': [0]*months, 'savings': [0]*months}

def get_cashflow_data(user, months=6):
    now = timezone.now().date()
    cashflow = []
    month_labels = []
    for i in range(months-1, -1, -1):
        start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        exp = Transaction.objects.filter(user=user, type='expense', date__gte=start, date__lt=end).aggregate(Sum('amount'))['amount__sum'] or 0
        inc = Transaction.objects.filter(user=user, type='income', date__gte=start, date__lt=end).aggregate(Sum('amount'))['amount__sum'] or 0
        cashflow.append(inc - exp)
        month_labels.append(start.strftime('%b %Y'))
    return {'labels': month_labels, 'cashflow': [float(c) for c in cashflow]}

def get_spending_trends(user):
    """Return daily, weekly, monthly spending aggregates."""
    now = timezone.now().date()
    start_daily = now - timedelta(days=30)
    daily = Transaction.objects.filter(
        user=user, type='expense', date__gte=start_daily
    ).values('date').annotate(total=Sum('amount')).order_by('date')
    daily_data = [{'date': d['date'].isoformat(), 'amount': float(d['total'])} for d in daily]

    # Weekly (last 12 weeks)
    weekly = []
    for i in range(11, -1, -1):
        week_start = now - timedelta(days=now.weekday() + 7*i)
        week_end = week_start + timedelta(days=6)
        total = Transaction.objects.filter(
            user=user, type='expense', date__gte=week_start, date__lte=week_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly.append({
            'week': f"Week {12-i}",
            'amount': float(total)
        })

    monthly = []
    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        total = Transaction.objects.filter(
            user=user, type='expense', date__gte=month_start, date__lt=month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly.append({
            'month': month_start.strftime('%b %Y'),
            'amount': float(total)
        })

    return {
        'daily': daily_data,
        'weekly': weekly,
        'monthly': monthly
    }

def get_income_trends(user):
    now = timezone.now().date()
    monthly = []
    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        total = Transaction.objects.filter(
            user=user, type='income', date__gte=month_start, date__lt=month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly.append({
            'month': month_start.strftime('%b %Y'),
            'amount': float(total)
        })
    # Income growth rate (last 3 months)
    if len(monthly) >= 3:
        recent = monthly[-1]['amount']
        older = monthly[-3]['amount']
        growth = ((recent - older) / older * 100) if older > 0 else 0
    else:
        growth = 0
    return {'monthly': monthly, 'growth_rate': round(growth, 2)}

def get_savings_analytics(user):
    now = timezone.now().date()
    # Savings rate (all time)
    total_income = Transaction.objects.filter(user=user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expense
    savings_rate = (savings / total_income * 100) if total_income > 0 else 0

    # Monthly savings trend
    monthly_savings = []
    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        inc = Transaction.objects.filter(user=user, type='income', date__gte=month_start, date__lt=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
        exp = Transaction.objects.filter(user=user, type='expense', date__gte=month_start, date__lt=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_savings.append({
            'month': month_start.strftime('%b %Y'),
            'savings': float(inc - exp)
        })

    # Projection (simple linear regression on savings)
    if len(monthly_savings) >= 3:
        y = [m['savings'] for m in monthly_savings]
        x = np.array(range(len(y))).reshape(-1,1)
        model = LinearRegression().fit(x, y)
        next_savings = model.predict([[len(y)]])[0]
        projection = round(next_savings, 2)
    else:
        projection = 0

    return {
        'savings_rate': round(savings_rate, 2),
        'monthly_savings': monthly_savings,
        'projection': projection
    }

def get_comparison_data(user):
    now = timezone.now().date()
    current_month_start = now.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)

    curr_inc = Transaction.objects.filter(user=user, type='income', date__gte=current_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    curr_exp = Transaction.objects.filter(user=user, type='expense', date__gte=current_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    prev_inc = Transaction.objects.filter(user=user, type='income', date__gte=last_month_start, date__lte=last_month_end).aggregate(Sum('amount'))['amount__sum'] or 0
    prev_exp = Transaction.objects.filter(user=user, type='expense', date__gte=last_month_start, date__lte=last_month_end).aggregate(Sum('amount'))['amount__sum'] or 0

    inc_change = ((curr_inc - prev_inc) / prev_inc * 100) if prev_inc > 0 else 0
    exp_change = ((curr_exp - prev_exp) / prev_exp * 100) if prev_exp > 0 else 0

    # Year comparison
    current_year = now.year
    last_year = current_year - 1
    curr_year_inc = Transaction.objects.filter(user=user, type='income', date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    curr_year_exp = Transaction.objects.filter(user=user, type='expense', date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    last_year_inc = Transaction.objects.filter(user=user, type='income', date__year=last_year).aggregate(Sum('amount'))['amount__sum'] or 0
    last_year_exp = Transaction.objects.filter(user=user, type='expense', date__year=last_year).aggregate(Sum('amount'))['amount__sum'] or 0

    year_inc_change = ((curr_year_inc - last_year_inc) / last_year_inc * 100) if last_year_inc > 0 else 0
    year_exp_change = ((curr_year_exp - last_year_exp) / last_year_exp * 100) if last_year_exp > 0 else 0

    return {
        'month': {
            'income': float(curr_inc),
            'expense': float(curr_exp),
            'prev_income': float(prev_inc),
            'prev_expense': float(prev_exp),
            'income_change': round(inc_change, 2),
            'expense_change': round(exp_change, 2)
        },
        'year': {
            'income': float(curr_year_inc),
            'expense': float(curr_year_exp),
            'prev_income': float(last_year_inc),
            'prev_expense': float(last_year_exp),
            'income_change': round(year_inc_change, 2),
            'expense_change': round(year_exp_change, 2)
        }
    }