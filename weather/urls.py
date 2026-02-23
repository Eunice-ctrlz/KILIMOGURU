from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.WeatherDashboardView.as_view(), name='dashboard'),
    path('<str:county>/', views.CountyWeatherView.as_view(), name='county_weather'),
    path('forecast/<str:county>/', views.WeatherForecastView.as_view(), name='forecast'),
    path('alerts/', views.ClimateAlertsView.as_view(), name='alerts'),
    path('alerts/<int:pk>/', views.AlertDetailView.as_view(), name='alert_detail'),
    path('subscribe/', views.SubscribeAlertsView.as_view(), name='subscribe'),
    path('irrigation/', views.IrrigationAdviceView.as_view(), name='irrigation'),
    path('api/current/', views.CurrentWeatherAPIView.as_view(), name='api_current'),
]
