from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class WeatherData(models.Model):
    """Weather data for different locations"""
    
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True, null=True)
    
    # Coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Current weather
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.PositiveIntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    
    # Conditions
    weather_condition = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=100)
    weather_icon = models.CharField(max_length=20, blank=True, null=True)
    
    # Wind
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wind_direction = models.PositiveIntegerField(blank=True, null=True)
    
    # Visibility
    visibility = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Clouds
    cloud_coverage = models.PositiveIntegerField(blank=True, null=True)
    
    # Rain
    rain_1h = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rain_3h = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    # Timestamp
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Weather Data'
        verbose_name_plural = 'Weather Data'
        ordering = ['-timestamp']
        unique_together = ['county', 'sub_county', 'timestamp']
    
    def __str__(self):
        return f"{self.county} - {self.temperature}°C - {self.timestamp}"


class WeatherForecast(models.Model):
    """Weather forecasts"""
    
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True, null=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Forecast details
    forecast_date = models.DateField()
    forecast_time = models.TimeField()
    
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2)
    
    humidity = models.PositiveIntegerField(blank=True, null=True)
    
    weather_condition = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=100)
    weather_icon = models.CharField(max_length=20, blank=True, null=True)
    
    # Precipitation
    precipitation_probability = models.PositiveIntegerField(default=0)
    precipitation_amount = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    
    # Wind
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Weather Forecast'
        verbose_name_plural = 'Weather Forecasts'
        ordering = ['forecast_date', 'forecast_time']
        unique_together = ['county', 'sub_county', 'forecast_date', 'forecast_time']
    
    def __str__(self):
        return f"{self.county} - {self.forecast_date} - {self.weather_condition}"


class ClimateAlert(models.Model):
    """Climate alerts and warnings"""
    
    ALERT_TYPES = [
        ('drought', 'Drought Warning'),
        ('flood', 'Flood Warning'),
        ('heavy_rain', 'Heavy Rain Warning'),
        ('frost', 'Frost Warning'),
        ('heatwave', 'Heatwave Warning'),
        ('strong_wind', 'Strong Wind Warning'),
        ('pest_outbreak', 'Pest Outbreak Alert'),
        ('disease_outbreak', 'Disease Outbreak Alert'),
        ('planting', 'Planting Advisory'),
        ('harvest', 'Harvest Advisory'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('severe', 'Severe'),
        ('extreme', 'Extreme'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Affected areas
    counties = models.JSONField(default=list)
    specific_areas = models.TextField(blank=True)
    
    # Timing
    issued_at = models.DateTimeField(auto_now_add=True)
    effective_from = models.DateTimeField()
    expires_at = models.DateTimeField()
    
    # Recommendations
    recommended_actions = models.TextField()
    crops_affected = models.JSONField(default=list, blank=True)
    
    # Source
    source = models.CharField(max_length=100, default='KMD')
    source_url = models.URLField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Climate Alert'
        verbose_name_plural = 'Climate Alerts'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"


class UserWeatherSubscription(models.Model):
    """User weather alert subscriptions"""
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='weather_subscriptions'
    )
    
    # Location
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True, null=True)
    
    # Alert preferences
    alert_types = models.JSONField(default=list)
    min_severity = models.CharField(
        max_length=10,
        choices=ClimateAlert.SEVERITY_LEVELS,
        default='moderate'
    )
    
    # Notification methods
    sms_alerts = models.BooleanField(default=True)
    email_alerts = models.BooleanField(default=False)
    push_alerts = models.BooleanField(default=True)
    
    # Crops of interest
    crops = models.JSONField(default=list, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Weather Subscription'
        verbose_name_plural = 'Weather Subscriptions'
        unique_together = ['user', 'county', 'sub_county']
    
    def __str__(self):
        return f"{self.user.username} - {self.county}"


class IrrigationAdvice(models.Model):
    """Irrigation advice based on weather"""
    
    crop = models.ForeignKey(
        'crops.Crop', on_delete=models.CASCADE, related_name='irrigation_advice'
    )
    
    # Conditions
    soil_type = models.CharField(max_length=20, choices=[
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loam', 'Loam'),
        ('silt', 'Silt'),
    ])
    
    growth_stage = models.CharField(
        max_length=20,
        choices=[
            ('germination', 'Germination'),
            ('vegetative', 'Vegetative'),
            ('flowering', 'Flowering'),
            ('fruiting', 'Fruiting'),
            ('maturity', 'Maturity'),
        ]
    )
    
    # Weather conditions
    temperature_range_min = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_range_max = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Advice
    irrigation_frequency = models.CharField(max_length=100)
    water_amount_mm = models.DecimalField(max_digits=5, decimal_places=2)
    best_time = models.CharField(max_length=100)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Irrigation Advice'
        verbose_name_plural = 'Irrigation Advice'
    
    def __str__(self):
        return f"{self.crop.name} - {self.growth_stage} - {self.soil_type}"
