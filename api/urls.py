from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'crops', views.CropViewSet)
router.register(r'produce', views.ProduceListingViewSet)
router.register(r'weather', views.WeatherDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    
    # Custom endpoints
    path('farmer/profile/', views.FarmerProfileAPIView.as_view(), name='farmer_profile'),
    path('farmer/crops/', views.FarmerCropsAPIView.as_view(), name='farmer_crops'),
    path('market/prices/', views.MarketPricesAPIView.as_view(), name='market_prices'),
    path('weather/current/', views.CurrentWeatherAPIView.as_view(), name='current_weather'),
    path('alerts/', views.AlertsAPIView.as_view(), name='alerts'),
]
