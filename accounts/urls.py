from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/farmer/', views.FarmerRegisterView.as_view(), name='register_farmer'),
    path('register/buyer/', views.BuyerRegisterView.as_view(), name='register_buyer'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='profile_edit'),
    path('verify-phone/', views.PhoneVerificationView.as_view(), name='verify_phone'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('devices/', views.UserDevicesView.as_view(), name='devices'),
    path('devices/<int:pk>/remove/', views.RemoveDeviceView.as_view(), name='remove_device'),
]
