from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView, ListView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
import string

from .models import User, UserDevice, OTPVerification
from .forms import (
    FarmerRegistrationForm, BuyerRegistrationForm, UserLoginForm,
    UserProfileForm, PhoneVerificationForm, PasswordResetRequestForm
)


class FarmerRegisterView(CreateView):
    """View for farmer registration"""
    model = User
    form_class = FarmerRegistrationForm
    template_name = 'accounts/register_farmer.html'
    success_url = reverse_lazy('accounts:verify_phone')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Inactive until phone verification
        user.save()
        
        # Generate and send OTP
        self.send_otp(user, 'registration')
        
        # Store user ID in session for verification
        self.request.session['verification_user_id'] = user.id
        self.request.session['verification_purpose'] = 'registration'
        
        messages.success(
            self.request,
            'Registration successful! Please verify your phone number with the OTP sent.'
        )
        return redirect('accounts:verify_phone')
    
    def send_otp(self, user, purpose):
        """Generate and send OTP"""
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        
        # TODO: Integrate with SMS gateway (Africa's Talking, Twilio, etc.)
        # For now, print to console for testing
        print(f"\n{'='*50}")
        print(f"OTP for {user.phone_number}: {otp_code}")
        print(f"{'='*50}\n")
        
        # Send SMS (placeholder)
        # sms_service.send_sms(user.phone_number, f"Your KILIMO GURU verification code is: {otp_code}")


class BuyerRegisterView(CreateView):
    """View for buyer registration"""
    model = User
    form_class = BuyerRegistrationForm
    template_name = 'accounts/register_buyer.html'
    success_url = reverse_lazy('accounts:verify_phone')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        self.send_otp(user, 'registration')
        
        self.request.session['verification_user_id'] = user.id
        self.request.session['verification_purpose'] = 'registration'
        
        messages.success(
            self.request,
            'Registration successful! Please verify your phone number.'
        )
        return redirect('accounts:verify_phone')
    
    def send_otp(self, user, purpose):
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        
        print(f"\n{'='*50}")
        print(f"OTP for {user.phone_number}: {otp_code}")
        print(f"{'='*50}\n")


class UserLoginView(View):
    """Custom login view"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Try to authenticate
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    # Register device for offline sync
                    self.register_device(request, user)
                    
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    
                    # Redirect based on user type
                    if user.is_farmer:
                        return redirect('farmers:dashboard')
                    elif user.is_buyer:
                        return redirect('marketplace:buyer_dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Your account is not active. Please verify your phone number.')
                    return redirect('accounts:verify_phone')
            else:
                messages.error(request, 'Invalid phone number or password.')
        
        return render(request, self.template_name, {'form': form})
    
    def register_device(self, request, user):
        """Register user device for offline sync"""
        device_id = request.META.get('HTTP_USER_AGENT', 'unknown')
        
        UserDevice.objects.get_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'device_type': 'web',
                'device_name': request.META.get('HTTP_USER_AGENT', 'Web Browser')[:100]
            }
        )


class UserLogoutView(LoginRequiredMixin, View):
    """Logout view"""
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')
    
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')


class PhoneVerificationView(View):
    """View for phone verification via OTP"""
    template_name = 'accounts/verify_phone.html'
    
    def get(self, request):
        form = PhoneVerificationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PhoneVerificationForm(request.POST)
        
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user_id = request.session.get('verification_user_id')
            purpose = request.session.get('verification_purpose', 'registration')
            
            if not user_id:
                messages.error(request, 'Session expired. Please register again.')
                return redirect('accounts:register_farmer')
            
            try:
                user = User.objects.get(id=user_id)
                otp_record = OTPVerification.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    purpose=purpose,
                    is_used=False
                ).latest('created_at')
                
                if otp_record.is_expired:
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return render(request, self.template_name, {'form': form})
                
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()
                
                # Activate user
                user.is_active = True
                user.is_verified = True
                user.save()
                
                # Clear session
                del request.session['verification_user_id']
                del request.session['verification_purpose']
                
                messages.success(request, 'Phone verified successfully! You can now log in.')
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
            except OTPVerification.DoesNotExist:
                messages.error(request, 'Invalid OTP code.')
        
        return render(request, self.template_name, {'form': form})


class ResendOTPView(View):
    """View to resend OTP"""
    
    def get(self, request):
        user_id = request.session.get('verification_user_id')
        purpose = request.session.get('verification_purpose', 'registration')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                
                # Invalidate old OTPs
                OTPVerification.objects.filter(
                    user=user,
                    purpose=purpose,
                    is_used=False
                ).update(is_used=True)
                
                # Generate new OTP
                otp_code = ''.join(random.choices(string.digits, k=6))
                expires_at = timezone.now() + timezone.timedelta(minutes=10)
                
                OTPVerification.objects.create(
                    user=user,
                    otp_code=otp_code,
                    purpose=purpose,
                    expires_at=expires_at
                )
                
                print(f"\n{'='*50}")
                print(f"New OTP for {user.phone_number}: {otp_code}")
                print(f"{'='*50}\n")
                
                messages.success(request, 'New OTP has been sent to your phone.')
                
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('accounts:register_farmer')
        
        return redirect('accounts:verify_phone')


class UserProfileView(LoginRequiredMixin, View):
    """View user profile"""
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class PasswordResetRequestView(View):
    """Request password reset"""
    template_name = 'accounts/password_reset.html'
    
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            # Normalize phone number
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            
            try:
                user = User.objects.get(phone_number=phone_number)
                
                # Generate OTP
                otp_code = ''.join(random.choices(string.digits, k=6))
                expires_at = timezone.now() + timezone.timedelta(minutes=10)
                
                OTPVerification.objects.create(
                    user=user,
                    otp_code=otp_code,
                    purpose='password_reset',
                    expires_at=expires_at
                )
                
                request.session['reset_user_id'] = user.id
                
                print(f"\n{'='*50}")
                print(f"Password Reset OTP for {user.phone_number}: {otp_code}")
                print(f"{'='*50}\n")
                
                messages.success(request, 'OTP has been sent to your phone.')
                return redirect('accounts:password_reset_confirm')
                
            except User.DoesNotExist:
                messages.error(request, 'No account found with this phone number.')
        
        return render(request, self.template_name, {'form': form})


class PasswordResetConfirmView(View):
    """Confirm password reset with OTP"""
    template_name = 'accounts/password_reset_confirm.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        otp_code = request.POST.get('otp_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user_id = request.session.get('reset_user_id')
        
        if not user_id:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('accounts:password_reset')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)
        
        try:
            user = User.objects.get(id=user_id)
            otp_record = OTPVerification.objects.filter(
                user=user,
                otp_code=otp_code,
                purpose='password_reset',
                is_used=False
            ).latest('created_at')
            
            if otp_record.is_expired:
                messages.error(request, 'OTP has expired.')
                return render(request, self.template_name)
            
            otp_record.is_used = True
            otp_record.save()
            
            user.set_password(new_password)
            user.save()
            
            del request.session['reset_user_id']
            
            messages.success(request, 'Password reset successful! Please log in.')
            return redirect('accounts:login')
            
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            messages.error(request, 'Invalid OTP code.')
        
        return render(request, self.template_name)


class ChangePasswordView(LoginRequiredMixin, View):
    """Change password for logged in user"""
    template_name = 'accounts/change_password.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return render(request, self.template_name)
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return render(request, self.template_name)
        
        request.user.set_password(new_password)
        request.user.save()
        
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Password changed successfully!')
        return redirect('accounts:profile')


class UserDevicesView(LoginRequiredMixin, ListView):
    """List user's registered devices"""
    model = UserDevice
    template_name = 'accounts/devices.html'
    context_object_name = 'devices'
    
    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)


class RemoveDeviceView(LoginRequiredMixin, View):
    """Remove a registered device"""
    
    def post(self, request, pk):
        device = get_object_or_404(UserDevice, pk=pk, user=request.user)
        device.delete()
        messages.success(request, 'Device removed successfully.')
        return redirect('accounts:devices')
