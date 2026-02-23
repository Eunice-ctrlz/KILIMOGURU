from rest_framework import serializers
from crops.models import Crop, FarmerCrop
from marketplace.models import ProduceListing, MarketPrice
from weather.models import WeatherData, ClimateAlert
from farmers.models import FarmerProfile


class CropSerializer(serializers.ModelSerializer):
    """Serializer for crops"""
    
    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'local_name', 'scientific_name', 'category',
            'optimal_temperature_min', 'optimal_temperature_max',
            'rainfall_requirement_min', 'rainfall_requirement_max',
            'growing_period_days', 'description', 'image'
        ]


class FarmerCropSerializer(serializers.ModelSerializer):
    """Serializer for farmer crops"""
    
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    
    class Meta:
        model = FarmerCrop
        fields = [
            'id', 'crop', 'crop_name', 'variety', 'season', 'year',
            'planting_date', 'expected_harvest_date', 'area_planted',
            'status', 'expected_yield', 'actual_yield'
        ]


class ProduceListingSerializer(serializers.ModelSerializer):
    """Serializer for produce listings"""
    
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    
    class Meta:
        model = ProduceListing
        fields = [
            'id', 'product_name', 'category', 'variety',
            'quantity_available', 'unit', 'price_per_unit',
            'quality_grade', 'is_organic', 'county',
            'farmer_name', 'image_1'
        ]


class MarketPriceSerializer(serializers.ModelSerializer):
    """Serializer for market prices"""
    
    class Meta:
        model = MarketPrice
        fields = [
            'id', 'product_name', 'category', 'market',
            'unit', 'min_price', 'max_price', 'average_price', 'price_date'
        ]


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer for weather data"""
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'county', 'temperature', 'feels_like', 'humidity',
            'weather_condition', 'weather_description', 'wind_speed',
            'rain_1h', 'timestamp'
        ]


class FarmerProfileSerializer(serializers.ModelSerializer):
    """Serializer for farmer profile"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'user_name', 'farm_name', 'farm_size', 'farm_size_unit',
            'farm_location', 'soil_type', 'farming_type',
            'irrigation_method', 'credit_score', 'credit_limit'
        ]


class ClimateAlertSerializer(serializers.ModelSerializer):
    """Serializer for climate alerts"""
    
    class Meta:
        model = ClimateAlert
        fields = [
            'id', 'alert_type', 'severity', 'title', 'description',
            'counties', 'recommended_actions', 'issued_at', 'expires_at'
        ]
