from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # additional fields (e.g., currency preference)
    currency = models.CharField(max_length=3, default='TND')
    
    def __str__(self):
        return self.username