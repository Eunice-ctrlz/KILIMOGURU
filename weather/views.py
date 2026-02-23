from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from .models import WeatherData, WeatherForecast, ClimateAlert, UserWeatherSubscription
from .forms import WeatherSubscriptionForm


class WeatherDashboardView(TemplateView):
    """Weather dashboard"""
    template_name = 'weather/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get major counties weather
        major_counties = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret']
        context['major_weather'] = WeatherData.objects.filter(
            county__in=major_counties
        ).order_by('-timestamp').distinct('county')[:5]
        
        # Active alerts
        context['active_alerts'] = ClimateAlert.objects.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )[:5]
        
        # All counties for search
        context['counties'] = WeatherData.objects.values_list(
            'county', flat=True
        ).distinct()
        
        return context


class CountyWeatherView(View):
    """Weather for specific county"""
    template_name = 'weather/county_weather.html'
    
    def get(self, request, county):
        # Get current weather
        try:
            current = WeatherData.objects.filter(
                county__iexact=county
            ).latest('timestamp')
        except WeatherData.DoesNotExist:
            current = None
        
        # Get forecast
        forecast = WeatherForecast.objects.filter(
            county__iexact=county,
            forecast_date__gte=timezone.now().date()
        )[:7]
        
        # Get alerts
        alerts = ClimateAlert.objects.filter(
            counties__contains=[county],
            is_active=True,
            expires_at__gt=timezone.now()
        )
        
        context = {
            'county': county,
            'current': current,
            'forecast': forecast,
            'alerts': alerts,
        }
        
        return render(request, self.template_name, context)


class WeatherForecastView(View):
    """Detailed weather forecast"""
    template_name = 'weather/forecast.html'
    
    def get(self, request, county):
        # Get 7-day forecast
        forecast = WeatherForecast.objects.filter(
            county__iexact=county,
            forecast_date__gte=timezone.now().date()
        ).order_by('forecast_date', 'forecast_time')
        
        # Group by date
        daily_forecast = {}
        for f in forecast:
            date_key = f.forecast_date.strftime('%Y-%m-%d')
            if date_key not in daily_forecast:
                daily_forecast[date_key] = {
                    'date': f.forecast_date,
                    'forecasts': []
                }
            daily_forecast[date_key]['forecasts'].append(f)
        
        context = {
            'county': county,
            'daily_forecast': daily_forecast.values(),
        }
        
        return render(request, self.template_name, context)


class ClimateAlertsView(ListView):
    """List climate alerts"""
    model = ClimateAlert
    template_name = 'weather/alerts.html'
    context_object_name = 'alerts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ClimateAlert.objects.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )
        
        # Filter by type
        alert_type = self.request.GET.get('type')
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        
        # Filter by severity
        severity = self.request.GET.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        return queryset.order_by('-issued_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alert_types'] = ClimateAlert.ALERT_TYPES
        context['severity_levels'] = ClimateAlert.SEVERITY_LEVELS
        return context


class AlertDetailView(DetailView):
    """Alert details"""
    model = ClimateAlert
    template_name = 'weather/alert_detail.html'
    context_object_name = 'alert'


class SubscribeAlertsView(LoginRequiredMixin, CreateView):
    """Subscribe to weather alerts"""
    model = UserWeatherSubscription
    form_class = WeatherSubscriptionForm
    template_name = 'weather/subscribe.html'
    success_url = '/weather/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Subscribed to weather alerts successfully!')
        return super().form_valid(form)


class IrrigationAdviceView(TemplateView):
    """Irrigation advice"""
    template_name = 'weather/irrigation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from crops.models import Crop
        context['crops'] = Crop.objects.filter(is_active=True)
        return context


class CurrentWeatherAPIView(View):
    """API endpoint for current weather"""
    
    def get(self, request):
        county = request.GET.get('county')
        
        if not county:
            return JsonResponse({'error': 'County parameter required'}, status=400)
        
        try:
            weather = WeatherData.objects.filter(
                county__iexact=county
            ).latest('timestamp')
            
            return JsonResponse({
                'county': weather.county,
                'temperature': float(weather.temperature),
                'humidity': weather.humidity,
                'condition': weather.weather_condition,
                'description': weather.weather_description,
                'wind_speed': float(weather.wind_speed) if weather.wind_speed else None,
                'timestamp': weather.timestamp.isoformat(),
            })
            
        except WeatherData.DoesNotExist:
            return JsonResponse({'error': 'No weather data available'}, status=404)
