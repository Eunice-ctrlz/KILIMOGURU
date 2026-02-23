from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MPesaTransaction(models.Model):
    """M-Pesa transaction records"""
    
    TRANSACTION_TYPES = [
        ('paybill', 'Paybill'),
        ('buy_goods', 'Buy Goods'),
        ('send_money', 'Send Money'),
        ('receive_money', 'Receive Money'),
        ('withdraw', 'Withdraw'),
        ('deposit', 'Deposit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mpesa_transactions'
    )
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # M-Pesa reference
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Phone numbers
    phone_number = models.CharField(max_length=15)
    recipient_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_description = models.TextField(blank=True)
    
    # Related to
    related_listing = models.ForeignKey(
        'marketplace.ProduceListing',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    related_transaction = models.ForeignKey(
        'marketplace.Transaction',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'M-Pesa Transaction'
        verbose_name_plural = 'M-Pesa Transactions'
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - KES {self.amount} - {self.status}"


class LoanProduct(models.Model):
    """Available loan products"""
    
    LOAN_TYPES = [
        ('input', 'Input Financing'),
        ('seasonal', 'Seasonal Loan'),
        ('equipment', 'Equipment Loan'),
        ('emergency', 'Emergency Loan'),
        ('insurance', 'Insurance Premium Financing'),
    ]
    
    name = models.CharField(max_length=100)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    description = models.TextField()
    
    # Terms
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_type = models.CharField(
        max_length=20,
        choices=[
            ('flat', 'Flat Rate'),
            ('reducing_balance', 'Reducing Balance'),
        ],
        default='flat'
    )
    
    # Duration
    min_duration_days = models.PositiveIntegerField()
    max_duration_days = models.PositiveIntegerField()
    
    # Requirements
    min_credit_score = models.IntegerField(default=0)
    requires_collateral = models.BooleanField(default=False)
    collateral_description = models.TextField(blank=True)
    
    # Provider
    provider_name = models.CharField(max_length=100)
    provider_logo = models.ImageField(upload_to='providers/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Loan Product'
        verbose_name_plural = 'Loan Products'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.provider_name}"


class LoanApplication(models.Model):
    """Farmer loan applications"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('active', 'Active'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='loan_applications'
    )
    loan_product = models.ForeignKey(
        LoanProduct, on_delete=models.CASCADE, related_name='applications'
    )
    
    # Application details
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    amount_approved = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    duration_days = models.PositiveIntegerField()
    
    # Purpose
    purpose = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Review
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='reviewed_loans'
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    
    # Disbursement
    disbursed_amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    disbursed_at = models.DateTimeField(blank=True, null=True)
    disbursement_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Repayment
    total_repaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_repayment_date = models.DateTimeField(blank=True, null=True)
    
    # Dates
    application_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.farmer.username} - {self.loan_product.name} - KES {self.amount_requested}"
    
    @property
    def outstanding_balance(self):
        if self.disbursed_amount:
            return self.disbursed_amount - self.total_repaid
        return 0
    
    @property
    def progress_percentage(self):
        if self.disbursed_amount and self.disbursed_amount > 0:
            return (self.total_repaid / self.disbursed_amount) * 100
        return 0


class LoanRepayment(models.Model):
    """Loan repayment records"""
    
    loan = models.ForeignKey(
        LoanApplication, on_delete=models.CASCADE, related_name='repayments'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    repayment_date = models.DateTimeField(auto_now_add=True)
    
    # Payment method
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('mpesa', 'M-Pesa'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash', 'Cash'),
            ('produce', 'Produce Offset'),
        ]
    )
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # M-Pesa link
    mpesa_transaction = models.ForeignKey(
        MPesaTransaction, on_delete=models.SET_NULL, blank=True, null=True
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Loan Repayment'
        verbose_name_plural = 'Loan Repayments'
        ordering = ['-repayment_date']
    
    def __str__(self):
        return f"KES {self.amount} - {self.loan.farmer.username}"


class InsuranceProduct(models.Model):
    """Agricultural insurance products"""
    
    INSURANCE_TYPES = [
        ('crop', 'Crop Insurance'),
        ('livestock', 'Livestock Insurance'),
        ('weather_index', 'Weather Index Insurance'),
        ('multi_peril', 'Multi-Peril Insurance'),
    ]
    
    name = models.CharField(max_length=100)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    description = models.TextField()
    
    # Coverage
    covered_crops = models.JSONField(default=list, blank=True)
    covered_livestock = models.JSONField(default=list, blank=True)
    covered_risks = models.JSONField(default=list)
    
    # Premium
    premium_rate = models.DecimalField(max_digits=5, decimal_places=2)
    min_sum_insured = models.DecimalField(max_digits=12, decimal_places=2)
    max_sum_insured = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Provider
    provider_name = models.CharField(max_length=100)
    provider_logo = models.ImageField(upload_to='providers/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Insurance Product'
        verbose_name_plural = 'Insurance Products'
    
    def __str__(self):
        return f"{self.name} - {self.provider_name}"


class InsurancePolicy(models.Model):
    """Insurance policies"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('claimed', 'Claimed'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='insurance_policies'
    )
    insurance_product = models.ForeignKey(
        InsuranceProduct, on_delete=models.CASCADE, related_name='policies'
    )
    
    # Policy details
    policy_number = models.CharField(max_length=50, unique=True)
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Coverage
    covered_items = models.JSONField(default=list)
    coverage_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Insurance Policy'
        verbose_name_plural = 'Insurance Policies'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.policy_number} - {self.farmer.username}"


class Wallet(models.Model):
    """User wallet for platform transactions"""
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet'
    )
    
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Limits
    daily_transaction_limit = models.DecimalField(
        max_digits=12, decimal_places=2, default=70000
    )
    monthly_transaction_limit = models.DecimalField(
        max_digits=12, decimal_places=2, default=140000
    )
    
    # Tracking
    daily_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f"{self.user.username} - KES {self.balance}"
    
    def can_transact(self, amount):
        """Check if user can make a transaction"""
        from datetime import date
        today = date.today()
        
        # Reset daily/monthly counters if needed
        if self.last_reset_date != today:
            self.daily_spent = 0
            if today.day == 1:
                self.monthly_spent = 0
            self.last_reset_date = today
            self.save()
        
        if self.daily_spent + amount > self.daily_transaction_limit:
            return False, "Daily transaction limit exceeded"
        
        if self.monthly_spent + amount > self.monthly_transaction_limit:
            return False, "Monthly transaction limit exceeded"
        
        return True, "OK"


class WalletTransaction(models.Model):
    """Wallet transaction records"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('transfer', 'Transfer'),
    ]
    
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions'
    )
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    
    description = models.CharField(max_length=200)
    reference = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - KES {self.amount}"
