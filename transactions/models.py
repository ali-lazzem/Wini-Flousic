from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Account'),
    ]
    CATEGORY_CHOICES = [
        ('drinks', 'Drinks'),
        ('food', 'Food'),
        ('snacks', 'Snacks'),
        ('transport', 'Transport'),
        ('fun', 'Fun'),
        ('university', 'University'),
        ('groceries', 'Groceries'),
        ('forgot', 'Forgot'),
        ('others', 'Others'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date}"
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
        ]