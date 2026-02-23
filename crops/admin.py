from django.contrib import admin
from .models import (
    Crop, CropVariety, FarmerCrop, PestDisease,
    PestDiseaseDetection, Livestock, LivestockProduction, PlantingCalendar
)


class CropVarietyInline(admin.TabularInline):
    model = CropVariety
    extra = 1


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'local_name', 'category', 'growing_period_days',
        'average_yield_per_acre', 'is_active'
    ]
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'local_name', 'scientific_name']
    inlines = [CropVarietyInline]


@admin.register(CropVariety)
class CropVarietyAdmin(admin.ModelAdmin):
    list_display = ['crop', 'name', 'is_drought_resistant', 'is_high_yielding']
    list_filter = ['is_drought_resistant', 'is_disease_resistant', 'is_high_yielding']
    search_fields = ['crop__name', 'name']


@admin.register(FarmerCrop)
class FarmerCropAdmin(admin.ModelAdmin):
    list_display = [
        'crop', 'farmer', 'season', 'year', 'status',
        'area_planted', 'actual_yield'
    ]
    list_filter = ['status', 'season', 'year', 'crop__category']
    search_fields = ['crop__name', 'farmer__username', 'farmer__phone_number']
    date_hierarchy = 'planting_date'


@admin.register(PestDisease)
class PestDiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'local_name', 'pest_disease_type', 'severity_level']
    list_filter = ['pest_disease_type', 'severity_level', 'is_active']
    search_fields = ['name', 'local_name', 'scientific_name']
    filter_horizontal = ['affected_crops']


@admin.register(PestDiseaseDetection)
class PestDiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = [
        'farmer', 'detected_pest_disease', 'confidence_score', 'is_verified', 'created_at'
    ]
    list_filter = ['is_verified', 'detected_pest_disease__pest_disease_type']
    search_fields = ['farmer__username', 'detected_pest_disease__name']
    date_hierarchy = 'created_at'


@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = [
        'species', 'breed', 'tag_number', 'name', 'gender',
        'is_healthy', 'is_active'
    ]
    list_filter = ['species', 'is_healthy', 'is_active', 'gender']
    search_fields = ['tag_number', 'name', 'breed']


@admin.register(LivestockProduction)
class LivestockProductionAdmin(admin.ModelAdmin):
    list_display = ['livestock', 'production_type', 'quantity', 'unit', 'production_date']
    list_filter = ['production_type']
    date_hierarchy = 'production_date'


@admin.register(PlantingCalendar)
class PlantingCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop', 'region']
    search_fields = ['crop__name', 'region']
