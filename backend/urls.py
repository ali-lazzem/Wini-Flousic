from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def api_root(request):
    return HttpResponse("Wini Flousic API - Use /api/transactions/ or /admin/")

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('transactions.urls')),
    path('api/auth/', include('core.urls')),
    path('api/predictions/', include('predictions.urls')),
    path('api/analytics/', include('financial_analytics.urls')),
]