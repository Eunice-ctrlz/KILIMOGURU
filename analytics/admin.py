from django.contrib import admin
from .models import FarmerAnalytics, MarketTrend, SystemMetric


@admin.register(FarmerAnalytics)
class FarmerAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'farmer', 'total_yield_current_year', 'net_profit_current_year',
        'profit_margin', 'last_updated'
    ]
    search_fields = ['farmer__username']


@admin.register(MarketTrend)
class MarketTrendAdmin(admin.ModelAdmin):
    list_display = [
        'product_name', 'market', 'current_avg_price',
        'price_change_percentage', 'created_at'
    ]
    list_filter = ['market', 'category']
    date_hierarchy = 'created_at'


@admin.register(SystemMetric)
class SystemMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'metric_value', 'category', 'date']
    list_filter = ['category']
    date_hierarchy = 'date'
