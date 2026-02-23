from django.contrib import admin
from .models import FarmerProfile, FarmParcel, FarmingHistory, CreditHistory


class FarmParcelInline(admin.TabularInline):
    model = FarmParcel
    extra = 1


class FarmingHistoryInline(admin.TabularInline):
    model = FarmingHistory
    extra = 0
    readonly_fields = ['created_at']


class CreditHistoryInline(admin.TabularInline):
    model = CreditHistory
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'farm_name', 'farm_size_display', 'farming_type',
        'irrigation_method', 'credit_score', 'is_subsidy_beneficiary'
    ]
    list_filter = [
        'farming_type', 'irrigation_method', 'soil_type',
        'is_subsidy_beneficiary', 'is_cooperative_member'
    ]
    search_fields = [
        'user__first_name', 'user__last_name', 'user__phone_number',
        'farm_name', 'farm_location'
    ]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [FarmParcelInline, FarmingHistoryInline, CreditHistoryInline]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Farm Details', {
            'fields': (
                'farm_name', 'farm_size', 'farm_size_unit',
                'farm_location', 'latitude', 'longitude'
            )
        }),
        ('Soil Information', {
            'fields': ('soil_type', 'soil_ph', 'soil_fertility')
        }),
        ('Farming Details', {
            'fields': ('farming_type', 'irrigation_method', 'years_of_experience')
        }),
        ('Financial Information', {
            'fields': (
                'annual_income', 'has_loan', 'loan_amount',
                'credit_score', 'credit_limit'
            )
        }),
        ('Subsidy & Cooperative', {
            'fields': (
                'is_subsidy_beneficiary', 'subsidy_type',
                'is_cooperative_member', 'cooperative_name'
            )
        }),
    )


@admin.register(FarmParcel)
class FarmParcelAdmin(admin.ModelAdmin):
    list_display = ['parcel_name', 'farmer_profile', 'size', 'current_crop', 'is_active']
    list_filter = ['is_active', 'soil_type']
    search_fields = ['parcel_name', 'farmer_profile__user__first_name', 'current_crop']


@admin.register(FarmingHistory)
class FarmingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'crop_name', 'farmer_profile', 'season', 'year',
        'actual_yield', 'yield_unit', 'profit'
    ]
    list_filter = ['season', 'year', 'crop_name']
    search_fields = ['crop_name', 'farmer_profile__user__first_name']
    date_hierarchy = 'planting_date'


@admin.register(CreditHistory)
class CreditHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'loan_type', 'farmer_profile', 'loan_amount',
        'status', 'application_date', 'due_date'
    ]
    list_filter = ['loan_type', 'status']
    search_fields = ['farmer_profile__user__first_name', 'lender_name']
    date_hierarchy = 'application_date'
