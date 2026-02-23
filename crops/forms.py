from django import forms
from .models import (
    FarmerCrop, Livestock, LivestockProduction, PestDiseaseDetection
)
from farmers.models import FarmParcel


class FarmerCropForm(forms.ModelForm):
    """Form for farmer crop management"""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                profile = user.farmer_profile
                self.fields['parcel'].queryset = FarmParcel.objects.filter(
                    farmer_profile=profile
                )
            except:
                self.fields['parcel'].queryset = FarmParcel.objects.none()
    
    class Meta:
        model = FarmerCrop
        fields = [
            'crop', 'variety', 'parcel', 'season', 'year',
            'planting_date', 'expected_harvest_date', 'area_planted',
            'planting_density', 'seed_quantity_used', 'notes'
        ]
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-select'}),
            'variety': forms.Select(attrs={'class': 'form-select'}),
            'parcel': forms.Select(attrs={'class': 'form-select'}),
            'season': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'planting_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'expected_harvest_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'area_planted': forms.NumberInput(attrs={'class': 'form-input'}),
            'planting_density': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 75cm x 30cm'
            }),
            'seed_quantity_used': forms.NumberInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3
            }),
        }


class LivestockForm(forms.ModelForm):
    """Form for livestock management"""
    
    class Meta:
        model = Livestock
        fields = [
            'species', 'breed', 'tag_number', 'name', 'gender',
            'date_of_birth', 'date_acquired', 'acquisition_method',
            'is_for_breeding', 'is_for_meat', 'is_for_milk', 'is_for_eggs',
            'health_notes'
        ]
        widgets = {
            'species': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Friesian, Boran'
            }),
            'tag_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ear tag or identification number'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional name'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'date_acquired': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'acquisition_method': forms.Select(attrs={'class': 'form-select'}),
            'is_for_breeding': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_for_meat': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_for_milk': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_for_eggs': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'health_notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Any health conditions or notes...'
            }),
        }


class LivestockProductionForm(forms.ModelForm):
    """Form for livestock production records"""
    
    class Meta:
        model = LivestockProduction
        fields = ['production_type', 'quantity', 'unit', 'market_value', 'notes']
        widgets = {
            'production_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'unit': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., liters, kg, pieces'
            }),
            'market_value': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Value in KES'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2
            }),
        }


class PestDiseaseDetectionForm(forms.ModelForm):
    """Form for pest/disease detection"""
    
    class Meta:
        model = PestDiseaseDetection
        fields = ['image', 'latitude', 'longitude']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional - GPS latitude'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional - GPS longitude'
            }),
        }
        help_texts = {
            'image': 'Upload a clear photo of the affected plant or pest'
        }
