from django.contrib import admin
from .models import (
    WeatherData, WeatherForecast, ClimateAlert,
    UserWeatherSubscription, IrrigationAdvice
)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['county', 'temperature', 'humidity', 'weather_condition', 'timestamp']
    list_filter = ['county', 'weather_condition']
    date_hierarchy = 'timestamp'


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ['county', 'forecast_date', 'temperature_min', 'temperature_max', 'precipitation_probability']
    list_filter = ['county']
    date_hierarchy = 'forecast_date'


@admin.register(ClimateAlert)
class ClimateAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'severity', 'title', 'issued_at', 'is_active']
    list_filter = ['alert_type', 'severity', 'is_active']
    date_hierarchy = 'issued_at'


@admin.register(UserWeatherSubscription)
class UserWeatherSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'county', 'min_severity', 'is_active']
    list_filter = ['is_active', 'min_severity']


@admin.register(IrrigationAdvice)
class IrrigationAdviceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'growth_stage', 'soil_type', 'water_amount_mm']
    list_filter = ['growth_stage', 'soil_type']
