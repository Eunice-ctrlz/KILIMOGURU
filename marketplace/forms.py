from django import forms
from .models import (
    ProduceListing, LivestockListing, BuyerInquiry,
    BuyerRequest, BuyerInquiry
)


class ProduceListingForm(forms.ModelForm):
    """Form for produce listings"""
    
    class Meta:
        model = ProduceListing
        fields = [
            'product_name', 'category', 'variety', 'description',
            'quantity_available', 'unit', 'price_per_unit', 'is_negotiable',
            'quality_grade', 'is_organic', 'certifications',
            'image_1', 'image_2', 'image_3',
            'county', 'sub_county', 'pickup_location',
            'available_from', 'available_until'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Fresh Maize'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'variety': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., H614'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe your produce...'
            }),
            'quantity_available': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 100'
            }),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Price in KES'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'quality_grade': forms.Select(attrs={'class': 'form-select'}),
            'is_organic': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'certifications': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'List any certifications (JSON format)'
            }),
            'image_1': forms.FileInput(attrs={'class': 'form-file'}),
            'image_2': forms.FileInput(attrs={'class': 'form-file'}),
            'image_3': forms.FileInput(attrs={'class': 'form-file'}),
            'county': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Kiambu'
            }),
            'sub_county': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Githunguri'
            }),
            'pickup_location': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Detailed pickup location'
            }),
            'available_from': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'available_until': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }


class LivestockListingForm(forms.ModelForm):
    """Form for livestock listings"""
    
    class Meta:
        model = LivestockListing
        fields = [
            'species', 'breed', 'age_months', 'weight_kg',
            'description', 'health_status', 'vaccination_status',
            'quantity', 'price_per_animal', 'is_negotiable',
            'image_1', 'image_2', 'image_3',
            'county', 'pickup_location'
        ]
        widgets = {
            'species': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Friesian'
            }),
            'age_months': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Age in months'
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Weight in kg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4
            }),
            'health_status': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2
            }),
            'vaccination_status': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2
            }),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'price_per_animal': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Price in KES'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'image_1': forms.FileInput(attrs={'class': 'form-file'}),
            'image_2': forms.FileInput(attrs={'class': 'form-file'}),
            'image_3': forms.FileInput(attrs={'class': 'form-file'}),
            'county': forms.TextInput(attrs={'class': 'form-input'}),
            'pickup_location': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2
            }),
        }


class BuyerInquiryForm(forms.ModelForm):
    """Form for buyer inquiries"""
    
    class Meta:
        model = BuyerInquiry
        fields = [
            'quantity_requested', 'proposed_price', 'message',
            'contact_phone', 'contact_email'
        ]
        widgets = {
            'quantity_requested': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Quantity you want to buy'
            }),
            'proposed_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your offered price per unit (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Your message to the farmer...'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your phone number'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your email (optional)'
            }),
        }


class BuyerRequestForm(forms.ModelForm):
    """Form for buyer requests"""
    
    class Meta:
        model = BuyerRequest
        fields = [
            'product_name', 'category', 'quantity_required', 'unit',
            'max_price_per_unit', 'quality_grade', 'requires_organic',
            'preferred_counties', 'required_by_date',
            'contact_phone', 'contact_email'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Fresh Tomatoes'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-input'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'max_price_per_unit': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Maximum price you can pay'
            }),
            'quality_grade': forms.Select(attrs={'class': 'form-select'}),
            'requires_organic': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'preferred_counties': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'List preferred counties (JSON)'
            }),
            'required_by_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class InquiryResponseForm(forms.ModelForm):
    """Form for responding to inquiries"""
    
    class Meta:
        model = BuyerInquiry
        fields = ['status', 'farmer_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'farmer_response': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Your response to the buyer...'
            }),
        }
