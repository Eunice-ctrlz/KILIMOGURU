from django import forms
from .models import UserWeatherSubscription


class WeatherSubscriptionForm(forms.ModelForm):
    """Form for weather alert subscription"""
    
    class Meta:
        model = UserWeatherSubscription
        fields = [
            'county', 'sub_county', 'alert_types', 'min_severity',
            'sms_alerts', 'email_alerts', 'push_alerts', 'crops'
        ]
        widgets = {
            'county': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your county'
            }),
            'sub_county': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your sub-county (optional)'
            }),
            'alert_types': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
            'min_severity': forms.Select(attrs={'class': 'form-select'}),
            'sms_alerts': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'email_alerts': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'push_alerts': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'crops': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Crops you are interested in (JSON)'
            }),
        }
