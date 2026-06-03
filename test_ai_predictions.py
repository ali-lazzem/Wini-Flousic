#!/usr/bin/env python
"""
One-time script to test AI prediction endpoints with fake data.
Run with: python test_ai_predictions.py
It will create a test user (if not exists) and populate fake transactions,
then display the API responses.
"""

import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from transactions.models import Transaction
from predictions.views import ExpensePredictionView, AIInsightsView
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

User = get_user_model()

TEST_USERNAME = 'ai_test_user'
TEST_PASSWORD = 'testpass123'

def create_test_user():
    user, created = User.objects.get_or_create(
        username=TEST_USERNAME,
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password(TEST_PASSWORD)
        user.save()
        print(f"Created test user: {TEST_USERNAME}")
    else:
        print(f"Using existing test user: {TEST_USERNAME}")
    return user

def delete_existing_transactions(user):
    """Optional: clear old transactions for this user"""
    count = Transaction.objects.filter(user=user).delete()[0]
    if count:
        print(f"Deleted {count} existing transactions for user {TEST_USERNAME}")
    else:
        print("No existing transactions to delete")

def generate_fake_transactions(user):
    """Generate 12 months of fake expenses and incomes"""
    categories = ['food', 'drinks', 'transport', 'fun', 'university', 'groceries', 'snacks', 'others']
    payment_methods = ['cash', 'bank']
    
    today = datetime.now().date()
    transactions = []
    
    # Generate monthly patterns
    for month_offset in range(12):
        month_start = (today.replace(day=1) - timedelta(days=30 * month_offset)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Random monthly income (between 500 and 1500 TND)
        monthly_income = random.uniform(500, 1500)
        # Random monthly expenses (between 300 and 1200 TND, usually less than income)
        monthly_expenses = random.uniform(300, min(1200, monthly_income * 0.9))
        
        # Create a single income transaction for the month (simplified)
        income_date = month_start + timedelta(days=random.randint(1, 5))
        transactions.append(Transaction(
            user=user,
            type='income',
            amount=monthly_income,
            category=None,
            description=f"Monthly income {month_start.strftime('%b %Y')}",
            date=income_date,
            payment_method=random.choice(payment_methods)
        ))
        
        # Create several expense transactions totaling monthly_expenses
        remaining = monthly_expenses
        expense_days = random.sample(range(1, 28), min(10, int(monthly_expenses / 20) + 2))
        expense_days.sort()
        for day in expense_days:
            if remaining <= 0:
                break
            # Random amount between 5 and 50, not exceeding remaining
            amount = min(random.uniform(5, 50), remaining)
            category = random.choice(categories)
            expense_date = month_start + timedelta(days=day - 1)
            transactions.append(Transaction(
                user=user,
                type='expense',
                amount=amount,
                category=category,
                description=f"Fake {category} expense",
                date=expense_date,
                payment_method=random.choice(payment_methods)
            ))
            remaining -= amount
        
        # If any leftover, add as one more expense
        if remaining > 0.1:
            expense_date = month_start + timedelta(days=random.randint(1, 28))
            transactions.append(Transaction(
                user=user,
                type='expense',
                amount=remaining,
                category=random.choice(categories),
                description=f"Remaining {remaining:.2f} expense",
                date=expense_date,
                payment_method=random.choice(payment_methods)
            ))
    
    # Bulk create for performance
    Transaction.objects.bulk_create(transactions)
    print(f"Created {len(transactions)} fake transactions for user {TEST_USERNAME}")

def test_predictions(user):
    """Call the prediction endpoints and print results"""
    factory = APIRequestFactory()
    
    # Test ExpensePredictionView
    request = factory.get('/api/predictions/expense-forecast/')
    request.user = user
    view = ExpensePredictionView.as_view()
    response = view(request)
    print("\n=== ExpensePredictionView Response ===")
    print(response.data)
    
    # Test AIInsightsView
    request = factory.get('/api/predictions/ai-insights/')
    request.user = user
    view = AIInsightsView.as_view()
    response = view(request)
    print("\n=== AIInsightsView Response ===")
    print(response.data)

def main():
    print("=== AI Prediction Test Script ===\n")
    user = create_test_user()
    
    # Optional: delete old transactions to start fresh
    delete_existing_transactions(user)
    
    generate_fake_transactions(user)
    test_predictions(user)
    
    print("\nTest completed. You can now log in as 'ai_test_user' to see the dashboard with fake data.")

if __name__ == '__main__':
    main()