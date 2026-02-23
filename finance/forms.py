from django import forms
from .models import MPesaTransaction, LoanApplication, InsurancePolicy, WalletTransaction


class MPesaPaymentForm(forms.ModelForm):
    """Form for M-Pesa payment"""
    
    class Meta:
        model = MPesaTransaction
        fields = ['transaction_type', 'amount', 'phone_number', 'recipient_phone']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Amount in KES'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your M-Pesa number'
            }),
            'recipient_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Recipient number (if sending)'
            }),
        }


class LoanApplicationForm(forms.ModelForm):
    """Form for loan application"""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                profile = user.farmer_profile
                self.fields['loan_product'].queryset = LoanProduct.objects.filter(
                    is_active=True,
                    min_credit_score__lte=profile.credit_score
                )
            except:
                pass
    
    class Meta:
        model = LoanApplication
        fields = ['loan_product', 'amount_requested', 'duration_days', 'purpose']
        widgets = {
            'loan_product': forms.Select(attrs={'class': 'form-select'}),
            'amount_requested': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Amount in KES'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Number of days'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Purpose of the loan...'
            }),
        }


class InsurancePurchaseForm(forms.ModelForm):
    """Form for insurance purchase"""
    
    class Meta:
        model = InsurancePolicy
        fields = [
            'insurance_product', 'sum_insured',
            'covered_items', 'coverage_area',
            'start_date', 'end_date'
        ]
        widgets = {
            'insurance_product': forms.Select(attrs={'class': 'form-select'}),
            'sum_insured': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Amount to insure'
            }),
            'covered_items': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Items to cover (JSON)'
            }),
            'coverage_area': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Area in acres'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }


class WalletDepositForm(forms.ModelForm):
    """Form for wallet deposit"""
    
    class Meta:
        model = WalletTransaction
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Amount to deposit'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional description'
            }),
        }
