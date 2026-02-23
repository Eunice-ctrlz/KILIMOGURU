from django import forms
from .models import ExpertConsultation, TeleVetConsultation, Webinar


class ConsultationBookingForm(forms.ModelForm):
    """Form for booking expert consultation"""
    
    class Meta:
        model = ExpertConsultation
        fields = [
            'topic', 'description', 'category',
            'requested_date', 'requested_time',
            'contact_method', 'contact_details'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What do you need help with?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe your question or problem in detail...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'requested_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'requested_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'contact_method': forms.Select(attrs={'class': 'form-select'}),
            'contact_details': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone number or email'
            }),
        }


class TeleVetConsultationForm(forms.ModelForm):
    """Form for tele-vet consultation"""
    
    class Meta:
        model = TeleVetConsultation
        fields = [
            'animal_species', 'animal_breed', 'animal_age',
            'symptoms', 'duration',
            'image_1', 'image_2', 'image_3'
        ]
        widgets = {
            'animal_species': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Cattle, Goat, Chicken'
            }),
            'animal_breed': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Friesian, Galla'
            }),
            'animal_age': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2 years, 6 months'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe the symptoms you observe...'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2 days, 1 week'
            }),
            'image_1': forms.FileInput(attrs={'class': 'form-file'}),
            'image_2': forms.FileInput(attrs={'class': 'form-file'}),
            'image_3': forms.FileInput(attrs={'class': 'form-file'}),
        }


class WebinarRegistrationForm(forms.ModelForm):
    """Form for webinar registration"""
    
    class Meta:
        model = Webinar
        fields = []  # Just for validation
