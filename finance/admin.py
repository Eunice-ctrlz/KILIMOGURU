from django.contrib import admin
from .models import (
    MPesaTransaction, LoanProduct, LoanApplication,
    LoanRepayment, InsuranceProduct, InsurancePolicy,
    Wallet, WalletTransaction
)


@admin.register(MPesaTransaction)
class MPesaTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'transaction_type', 'amount', 'status',
        'mpesa_receipt_number', 'initiated_at'
    ]
    list_filter = ['transaction_type', 'status']
    search_fields = ['user__username', 'mpesa_receipt_number', 'phone_number']
    date_hierarchy = 'initiated_at'


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_name', 'loan_type', 'min_amount', 'max_amount', 'is_active']
    list_filter = ['loan_type', 'is_active']


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'farmer', 'loan_product', 'amount_requested',
        'status', 'application_date', 'due_date'
    ]
    list_filter = ['status', 'loan_product__loan_type']
    date_hierarchy = 'application_date'


@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'repayment_date', 'payment_method']
    date_hierarchy = 'repayment_date'


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_name', 'insurance_type', 'premium_rate', 'is_active']
    list_filter = ['insurance_type', 'is_active']


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'farmer', 'insurance_product', 'sum_insured', 'status']
    list_filter = ['status', 'insurance_product__insurance_type']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'is_active', 'created_at']
    search_fields = ['user__username']


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transaction_type', 'amount', 'created_at']
    list_filter = ['transaction_type']
    date_hierarchy = 'created_at'
