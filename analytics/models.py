from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FarmerAnalytics(models.Model):
    """Analytics data for farmers"""
    
    farmer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='analytics'
    )
    
    # Yield analytics
    total_yield_current_year = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_yield_previous_year = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    yield_growth_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    
    # Financial analytics
    total_revenue_current_year = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_costs_current_year = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    net_profit_current_year = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Crop performance
    top_performing_crop = models.CharField(max_length=100, blank=True, null=True)
    top_crop_yield = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    
    # Land utilization
    total_farm_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    utilized_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Updated timestamp
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Farmer Analytics'
        verbose_name_plural = 'Farmers Analytics'
    
    def __str__(self):
        return f"Analytics for {self.farmer.username}"


class MarketTrend(models.Model):
    """Market trends and analysis"""
    
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    
    # Price trends
    current_avg_price = models.DecimalField(max_digits=10, decimal_places=2)
    previous_avg_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Volume trends
    current_volume = models.DecimalField(max_digits=12, decimal_places=2)
    previous_volume = models.DecimalField(max_digits=12, decimal_places=2)
    volume_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Market
    market = models.CharField(max_length=20)
    
    # Period
    period_start = models.DateField()
    period_end = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Market Trend'
        verbose_name_plural = 'Market Trends'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.market} - {self.period_start}"


class SystemMetric(models.Model):
    """System-wide metrics"""
    
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_unit = models.CharField(max_length=50, blank=True)
    
    # Category
    category = models.CharField(
        max_length=20,
        choices=[
            ('users', 'Users'),
            ('transactions', 'Transactions'),
            ('listings', 'Listings'),
            ('loans', 'Loans'),
            ('weather', 'Weather'),
            ('engagement', 'Engagement'),
        ]
    )
    
    # Period
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'System Metric'
        verbose_name_plural = 'System Metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.metric_name} - {self.metric_value} on {self.date}"
