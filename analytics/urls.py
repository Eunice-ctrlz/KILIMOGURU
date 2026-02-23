from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('yield/', views.YieldAnalyticsView.as_view(), name='yield'),
    path('profitability/', views.ProfitabilityView.as_view(), name='profitability'),
    path('market-trends/', views.MarketTrendsView.as_view(), name='market_trends'),
    path('farm-performance/', views.FarmPerformanceView.as_view(), name='farm_performance'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('api/data/', views.AnalyticsDataAPIView.as_view(), name='api_data'),
]
