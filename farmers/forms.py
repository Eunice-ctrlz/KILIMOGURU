from django import forms
from .models import FarmerProfile, FarmParcel, FarmingHistory, CreditHistory


class FarmerProfileForm(forms.ModelForm):
    """Form for editing farmer profile"""
    
    class Meta:
        model = FarmerProfile
        fields = [
            'farm_name', 'farm_size', 'farm_size_unit', 'farm_location',
            'latitude', 'longitude', 'soil_type', 'soil_ph', 'soil_fertility',
            'farming_type', 'irrigation_method', 'years_of_experience',
            'is_cooperative_member', 'cooperative_name'
        ]
        widgets = {
            'farm_name': forms.TextInput(attrs={'class': 'form-input'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-input'}),
            'farm_size_unit': forms.Select(attrs={'class': 'form-select'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-input'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input'}),
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'soil_ph': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1'}),
            'soil_fertility': forms.Select(attrs={'class': 'form-select'}),
            'farming_type': forms.Select(attrs={'class': 'form-select'}),
            'irrigation_method': forms.Select(attrs={'class': 'form-select'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_cooperative_member': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'cooperative_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class CompleteProfileForm(forms.ModelForm):
    """Form for completing farmer profile"""
    
    class Meta:
        model = FarmerProfile
        fields = [
            'farm_name', 'farm_size', 'farm_size_unit', 'farm_location',
            'latitude', 'longitude', 'soil_type', 'farming_type',
            'irrigation_method', 'years_of_experience'
        ]
        widgets = {
            'farm_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Green Valley Farm'
            }),
            'farm_size': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 5'
            }),
            'farm_size_unit': forms.Select(attrs={'class': 'form-select'}),
            'farm_location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Kiambu County, Githunguri'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional - e.g., -1.2921'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional - e.g., 36.8219'
            }),
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'farming_type': forms.Select(attrs={'class': 'form-select'}),
            'irrigation_method': forms.Select(attrs={'class': 'form-select'}),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 10'
            }),
        }


class FarmParcelForm(forms.ModelForm):
    """Form for creating/editing farm parcels"""
    
    class Meta:
        model = FarmParcel
        fields = [
            'parcel_name', 'size', 'size_unit', 'current_crop',
            'soil_type', 'soil_ph', 'notes'
        ]
        widgets = {
            'parcel_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., North Field'
            }),
            'size': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2.5'
            }),
            'size_unit': forms.Select(attrs={'class': 'form-select'}),
            'current_crop': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Maize'
            }),
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'soil_ph': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Any additional notes about this parcel...'
            }),
        }


class FarmingHistoryForm(forms.ModelForm):
    """Form for adding farming history"""
    
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
                pass
    
    class Meta:
        model = FarmingHistory
        fields = [
            'parcel', 'crop_name', 'crop_variety', 'season', 'year',
            'planting_date', 'harvest_date', 'area_planted',
            'expected_yield', 'actual_yield', 'yield_unit',
            'seed_variety', 'fertilizer_used', 'pesticides_used',
            'total_cost', 'total_revenue', 'notes'
        ]
        widgets = {
            'parcel': forms.Select(attrs={'class': 'form-select'}),
            'crop_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Maize'
            }),
            'crop_variety': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., H614'
            }),
            'season': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-input',
                'value': '2024'
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'harvest_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'area_planted': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2.5'
            }),
            'expected_yield': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 20'
            }),
            'actual_yield': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 18'
            }),
            'yield_unit': forms.Select(attrs={'class': 'form-select'}),
            'seed_variety': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Certified H614'
            }),
            'fertilizer_used': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'List fertilizers used...'
            }),
            'pesticides_used': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'List pesticides used...'
            }),
            'total_cost': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Total cost in KES'
            }),
            'total_revenue': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Total revenue in KES'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3
            }),
        }


class CreditApplicationForm(forms.ModelForm):
    """Form for applying for credit"""
    
    class Meta:
        model = CreditHistory
        fields = [
            'loan_type', 'loan_amount', 'lender_name',
            'application_date', 'due_date', 'notes'
        ]
        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-select'}),
            'loan_amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Amount in KES'
            }),
            'lender_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Equity Bank'
            }),
            'application_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Additional information...'
            }),
        }
