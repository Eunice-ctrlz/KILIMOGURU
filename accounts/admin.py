from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserDevice, OTPVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'get_full_name', 'phone_number', 'user_type', 
        'county', 'is_verified', 'is_active', 'date_joined'
    ]
    list_filter = [
        'user_type', 'is_verified', 'is_staff', 'is_active', 
        'preferred_language', 'gender', 'county'
    ]
    search_fields = [
        'username', 'first_name', 'last_name', 'phone_number', 
        'email', 'id_number', 'kiamis_id'
    ]
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('KILIMO GURU Info', {
            'fields': (
                'user_type', 'phone_number', 'id_number', 
                'date_of_birth', 'gender', 'preferred_language'
            )
        }),
        ('Location', {
            'fields': ('county', 'sub_county', 'ward', 'village')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'is_verified')
        }),
        ('KIAMIS Integration', {
            'fields': ('is_kiamis_registered', 'kiamis_id')
        }),
        ('M-Pesa', {
            'fields': ('mpesa_number',)
        }),
        ('Notifications', {
            'fields': ('sms_notifications', 'email_notifications')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'county')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'device_name', 'is_active', 'last_sync']
    list_filter = ['device_type', 'is_active']
    search_fields = ['user__username', 'user__phone_number', 'device_id']
    date_hierarchy = 'created_at'


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'purpose', 'is_used', 'expires_at', 'created_at']
    list_filter = ['purpose', 'is_used']
    search_fields = ['user__username', 'user__phone_number']
    date_hierarchy = 'created_at'
