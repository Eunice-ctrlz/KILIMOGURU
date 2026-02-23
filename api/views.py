from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from crops.models import Crop, FarmerCrop
from marketplace.models import ProduceListing, MarketPrice
from weather.models import WeatherData, ClimateAlert
from farmers.models import FarmerProfile
from .serializers import (
    CropSerializer, FarmerCropSerializer, ProduceListingSerializer,
    MarketPriceSerializer, WeatherDataSerializer, FarmerProfileSerializer,
    ClimateAlertSerializer
)


class CropViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for crops"""
    queryset = Crop.objects.filter(is_active=True)
    serializer_class = CropSerializer


class FarmerProfileAPIView(APIView):
    """API endpoint for farmer profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            profile = request.user.farmer_profile
            serializer = FarmerProfileSerializer(profile)
            return Response(serializer.data)
        except FarmerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)


class FarmerCropsAPIView(APIView):
    """API endpoint for farmer's crops"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        crops = FarmerCrop.objects.filter(farmer=request.user)
        serializer = FarmerCropSerializer(crops, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FarmerCropSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(farmer=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProduceListingViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for produce listings"""
    queryset = ProduceListing.objects.filter(status='active')
    serializer_class = ProduceListingSerializer


class MarketPricesAPIView(APIView):
    """API endpoint for market prices"""
    
    def get(self, request):
        from datetime import date, timedelta
        recent_date = date.today() - timedelta(days=7)
        
        prices = MarketPrice.objects.filter(price_date__gte=recent_date)
        
        # Filter by market
        market = request.GET.get('market')
        if market:
            prices = prices.filter(market=market)
        
        serializer = MarketPriceSerializer(prices, many=True)
        return Response(serializer.data)


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for weather data"""
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer


class CurrentWeatherAPIView(APIView):
    """API endpoint for current weather"""
    
    def get(self, request):
        county = request.GET.get('county')
        if not county:
            return Response({'error': 'County parameter required'}, status=400)
        
        try:
            weather = WeatherData.objects.filter(
                county__iexact=county
            ).latest('timestamp')
            serializer = WeatherDataSerializer(weather)
            return Response(serializer.data)
        except WeatherData.DoesNotExist:
            return Response({'error': 'No weather data available'}, status=404)


class AlertsAPIView(APIView):
    """API endpoint for climate alerts"""
    
    def get(self, request):
        from django.utils import timezone
        alerts = ClimateAlert.objects.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        )
        
        # Filter by county
        county = request.GET.get('county')
        if county:
            alerts = alerts.filter(counties__contains=[county])
        
        serializer = ClimateAlertSerializer(alerts, many=True)
        return Response(serializer.data)
