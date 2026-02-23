from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class FarmerRegistrationForm(UserCreationForm):
    """Registration form for farmers"""
    
    phone_regex = RegexValidator(
        regex=r'^(?:254|0)?[71]\d{8}$',
        message="Phone number must be in format: 2547XXXXXXXX or 07XXXXXXXX"
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone Number (e.g., 0712345678)'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address (Optional)'
        })
    )
    county = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'County'
        })
    )
    sub_county = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Sub-County'
        })
    )
    ward = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ward'
        })
    )
    preferred_language = forms.ChoiceField(
        choices=User.LANGUAGE_CHOICES,
        initial='en',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    id_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'National ID Number (Optional)'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'county', 'sub_county', 'ward', 'preferred_language',
            'id_number', 'password1', 'password2'
        ]
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Normalize phone number to start with 254
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
        
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'farmer'
        user.username = self.cleaned_data['phone_number']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
        return user


class BuyerRegistrationForm(UserCreationForm):
    """Registration form for buyers"""
    
    phone_regex = RegexValidator(
        regex=r'^(?:254|0)?[71]\d{8}$',
        message="Phone number must be in format: 2547XXXXXXXX or 07XXXXXXXX"
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone Number'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address'
        })
    )
    business_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Business Name'
        })
    )
    business_type = forms.ChoiceField(
        choices=[
            ('processor', 'Processor'),
            ('exporter', 'Exporter'),
            ('retailer', 'Retailer'),
            ('wholesaler', 'Wholesaler'),
            ('cooperative', 'Cooperative'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    county = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'County'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'business_name', 'business_type', 'county',
            'password1', 'password2'
        ]
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
        
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'buyer'
        user.username = self.cleaned_data['phone_number']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone Number or Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'preferred_language',
            'county', 'sub_county', 'ward', 'village',
            'profile_picture', 'mpesa_number',
            'sms_notifications', 'email_notifications'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'preferred_language': forms.Select(attrs={'class': 'form-select'}),
            'county': forms.TextInput(attrs={'class': 'form-input'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-input'}),
            'ward': forms.TextInput(attrs={'class': 'form-input'}),
            'village': forms.TextInput(attrs={'class': 'form-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-file'}),
            'mpesa_number': forms.TextInput(attrs={'class': 'form-input'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class PhoneVerificationForm(forms.Form):
    """Form for phone verification via OTP"""
    
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter 6-digit OTP'
        })
    )


class PasswordResetRequestForm(forms.Form):
    """Form for requesting password reset"""
    
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your phone number'
        })
    )
