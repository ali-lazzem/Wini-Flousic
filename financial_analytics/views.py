from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import (
    calculate_health_score, get_heatmap_data, get_forecast_data, get_cashflow_data,
    get_spending_trends, get_income_trends, get_savings_analytics, get_comparison_data
)

class HealthScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        score = calculate_health_score(request.user)
        return Response({'health_score': score})

class HeatmapView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        days = int(request.query_params.get('days', 90))
        data = get_heatmap_data(request.user, days)
        return Response({'data': data})

class ForecastView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        months = int(request.query_params.get('months', 6))
        data = get_forecast_data(request.user, months)
        return Response(data)

class CashflowView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        months = int(request.query_params.get('months', 6))
        data = get_cashflow_data(request.user, months)
        return Response(data)

class SpendingTrendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = get_spending_trends(request.user)
        return Response(data)

class IncomeTrendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = get_income_trends(request.user)
        return Response(data)

class SavingsAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = get_savings_analytics(request.user)
        return Response(data)

class ComparisonView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = get_comparison_data(request.user)
        return Response(data)