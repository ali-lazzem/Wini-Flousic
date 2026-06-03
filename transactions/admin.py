from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'category', 'date', 'payment_method')
    list_filter = ('type', 'category', 'payment_method', 'date')
    search_fields = ('description', 'user__username')