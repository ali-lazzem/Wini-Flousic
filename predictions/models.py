from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    predicted_expense = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_income = models.DecimalField(max_digits=10, decimal_places=2)
    risk_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deadline = models.DateField()
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.current_amount > self.target_amount:
            raise ValidationError({'current_amount': 'Current amount cannot exceed target amount.'})

    @property
    def progress_percent(self):
        if self.target_amount > 0:
            percent = (self.current_amount / self.target_amount) * 100
            return round(min(float(percent), 100.0), 2)
        return 0.0

    def __str__(self):
        return f"{self.name} - {self.user.username}"