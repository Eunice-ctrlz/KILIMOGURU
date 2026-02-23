from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User Model for KILIMO GURU"""
    
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('supplier', 'Supplier'),
        ('expert', 'Agricultural Expert'),
        ('admin', 'Administrator'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('sw', 'Swahili'),
        ('ki', 'Kikuyu'),
        ('lu', 'Luo'),
        ('ka', 'Kalenjin'),
        ('kl', 'Kamba'),
    ]
    
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default='farmer',
        verbose_name=_('User Type')
    )
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name=_('Phone Number')
    )
    email = models.EmailField(
        unique=True, 
        blank=True, 
        null=True,
        verbose_name=_('Email Address')
    )
    id_number = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name=_('National ID Number')
    )
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        verbose_name=_('Date of Birth')
    )
    gender = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True,
        verbose_name=_('Gender')
    )
    preferred_language = models.CharField(
        max_length=2, 
        choices=LANGUAGE_CHOICES, 
        default='en',
        verbose_name=_('Preferred Language')
    )
    county = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_('County')
    )
    sub_county = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_('Sub-County')
    )
    ward = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_('Ward')
    )
    village = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_('Village')
    )
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        verbose_name=_('Profile Picture')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Is Verified')
    )
    is_kiamis_registered = models.BooleanField(
        default=False,
        verbose_name=_('KIAMIS Registered')
    )
    kiamis_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_('KIAMIS ID')
    )
    mpesa_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name=_('M-Pesa Number')
    )
    sms_notifications = models.BooleanField(
        default=True,
        verbose_name=_('SMS Notifications')
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Email Notifications')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.phone_number or 'No Phone'})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_farmer(self):
        return self.user_type == 'farmer'
    
    @property
    def is_buyer(self):
        return self.user_type == 'buyer'
    
    @property
    def is_supplier(self):
        return self.user_type == 'supplier'


class UserDevice(models.Model):
    """Track user devices for offline sync and push notifications"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='devices'
    )
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('android', 'Android'),
            ('ios', 'iOS'),
            ('web', 'Web Browser'),
            ('feature_phone', 'Feature Phone'),
        ]
    )
    device_name = models.CharField(max_length=100, blank=True)
    fcm_token = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'device_id']
        verbose_name = 'User Device'
        verbose_name_plural = 'User Devices'
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type}"


class OTPVerification(models.Model):
    """OTP verification for phone number verification"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='otp_verifications'
    )
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(
        max_length=20,
        choices=[
            ('registration', 'Registration'),
            ('password_reset', 'Password Reset'),
            ('phone_verify', 'Phone Verification'),
            ('transaction', 'Transaction'),
        ]
    )
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
    
    def __str__(self):
        return f"{self.user.username} - {self.purpose}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
