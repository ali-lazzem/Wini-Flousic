from django.urls import path
from .views import (
    HealthScoreView, HeatmapView, ForecastView, CashflowView,
    SpendingTrendsView, IncomeTrendsView, SavingsAnalyticsView, ComparisonView
)

urlpatterns = [
    path('health/', HealthScoreView.as_view(), name='health'),
    path('heatmap/', HeatmapView.as_view(), name='heatmap'),
    path('forecast/', ForecastView.as_view(), name='forecast'),
    path('cashflow/', CashflowView.as_view(), name='cashflow'),
    path('spending-trends/', SpendingTrendsView.as_view(), name='spending-trends'),
    path('income-trends/', IncomeTrendsView.as_view(), name='income-trends'),
    path('savings-analytics/', SavingsAnalyticsView.as_view(), name='savings-analytics'),
    path('comparisons/', ComparisonView.as_view(), name='comparisons'),
]