from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpensePredictionView, MonthlyReviewView, GoalViewSet, AIInsightsView

router = DefaultRouter()
router.register('goals', GoalViewSet, basename='goal')

urlpatterns = [
    path('expense-forecast/', ExpensePredictionView.as_view(), name='expense-forecast'),
    path('ai-insights/', AIInsightsView.as_view(), name='ai-insights'),
    path('review/', MonthlyReviewView.as_view(), name='review'),
    path('', include(router.urls)),
]