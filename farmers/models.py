from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class FarmerProfile(models.Model):
    """Extended profile for farmers"""
    
    FARM_SIZE_UNITS = [
        ('acres', 'Acres'),
        ('hectares', 'Hectares'),
        ('sq_km', 'Square Kilometers'),
    ]
    
    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay Soil'),
        ('sandy', 'Sandy Soil'),
        ('loam', 'Loam Soil'),
        ('silt', 'Silt Soil'),
        ('peat', 'Peat Soil'),
        ('chalky', 'Chalky Soil'),
        ('black_cotton', 'Black Cotton Soil'),
        ('red', 'Red Soil'),
        ('alluvial', 'Alluvial Soil'),
        ('unknown', 'Unknown'),
    ]
    
    IRRIGATION_CHOICES = [
        ('rainfed', 'Rain-fed'),
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler Irrigation'),
        ('furrow', 'Furrow Irrigation'),
        ('flood', 'Flood Irrigation'),
        ('center_pivot', 'Center Pivot'),
        ('manual', 'Manual Watering'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='farmer_profile'
    )
    
    # Farm Details
    farm_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_('Farm Name')
    )
    farm_size = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name=_('Farm Size')
    )
    farm_size_unit = models.CharField(
        max_length=10, 
        choices=FARM_SIZE_UNITS, 
        default='acres',
        verbose_name=_('Farm Size Unit')
    )
    farm_location = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name=_('Farm Location')
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name=_('Longitude')
    )
    
    # Soil Information
    soil_type = models.CharField(
        max_length=20, 
        choices=SOIL_TYPE_CHOICES, 
        default='unknown',
        verbose_name=_('Soil Type')
    )
    soil_ph = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        blank=True, 
        null=True,
        verbose_name=_('Soil pH')
    )
    soil_fertility = models.CharField(
        max_length=20,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
            ('unknown', 'Unknown'),
        ],
        default='unknown',
        verbose_name=_('Soil Fertility')
    )
    
    # Farming Details
    farming_type = models.CharField(
        max_length=20,
        choices=[
            ('subsistence', 'Subsistence Farming'),
            ('commercial', 'Commercial Farming'),
            ('mixed', 'Mixed Farming'),
            ('organic', 'Organic Farming'),
        ],
        default='subsistence',
        verbose_name=_('Farming Type')
    )
    irrigation_method = models.CharField(
        max_length=20, 
        choices=IRRIGATION_CHOICES, 
        default='rainfed',
        verbose_name=_('Irrigation Method')
    )
    
    # Financial Information
    annual_income = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name=_('Annual Income (KES)')
    )
    has_loan = models.BooleanField(
        default=False,
        verbose_name=_('Has Active Loan')
    )
    loan_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name=_('Loan Amount (KES)')
    )
    
    # Credit Score
    credit_score = models.IntegerField(
        default=0,
        verbose_name=_('Credit Score')
    )
    credit_limit = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name=_('Credit Limit (KES)')
    )
    
    # Subsidy Information
    is_subsidy_beneficiary = models.BooleanField(
        default=False,
        verbose_name=_('Subsidy Beneficiary')
    )
    subsidy_type = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_('Subsidy Type')
    )
    
    # Additional Info
    years_of_experience = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Years of Experience')
    )
    is_cooperative_member = models.BooleanField(
        default=False,
        verbose_name=_('Cooperative Member')
    )
    cooperative_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_('Cooperative Name')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Farmer Profile')
        verbose_name_plural = _('Farmer Profiles')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.farm_name or 'Unnamed Farm'}"
    
    @property
    def farm_size_display(self):
        return f"{self.farm_size} {self.get_farm_size_unit_display()}"
    
    @property
    def location_display(self):
        if self.latitude and self.longitude:
            return f"{self.farm_location} ({self.latitude}, {self.longitude})"
        return self.farm_location


class FarmParcel(models.Model):
    """Individual farm parcels/sections"""
    
    farmer_profile = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='parcels'
    )
    parcel_name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    size_unit = models.CharField(
        max_length=10, 
        choices=FarmerProfile.FARM_SIZE_UNITS, 
        default='acres'
    )
    
    # GPS Coordinates (polygon points stored as JSON)
    boundary_coordinates = models.JSONField(
        blank=True, 
        null=True,
        help_text="GPS coordinates of parcel boundary"
    )
    
    # Current Status
    current_crop = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Soil details specific to parcel
    soil_type = models.CharField(
        max_length=20, 
        choices=FarmerProfile.SOIL_TYPE_CHOICES, 
        default='unknown'
    )
    soil_ph = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        blank=True, 
        null=True
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Farm Parcel'
        verbose_name_plural = 'Farm Parcels'
        ordering = ['parcel_name']
    
    def __str__(self):
        return f"{self.parcel_name} - {self.size} {self.get_size_unit_display()}"


class FarmingHistory(models.Model):
    """Historical farming data for crop rotation planning"""
    
    farmer_profile = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='farming_history'
    )
    parcel = models.ForeignKey(
        FarmParcel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='crop_history'
    )
    
    crop_name = models.CharField(max_length=100)
    crop_variety = models.CharField(max_length=100, blank=True, null=True)
    season = models.CharField(
        max_length=20,
        choices=[
            ('short_rains', 'Short Rains (Oct-Dec)'),
            ('long_rains', 'Long Rains (Mar-May)'),
            ('dry_season', 'Dry Season (Jun-Sep)'),
        ]
    )
    year = models.PositiveIntegerField()
    
    # Planting Details
    planting_date = models.DateField(blank=True, null=True)
    harvest_date = models.DateField(blank=True, null=True)
    area_planted = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    
    # Yield Information
    expected_yield = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    actual_yield = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    yield_unit = models.CharField(
        max_length=20,
        choices=[
            ('kg', 'Kilograms'),
            ('tonnes', 'Tonnes'),
            ('bags_90kg', 'Bags (90kg)'),
            ('bags_50kg', 'Bags (50kg)'),
        ],
        default='kg'
    )
    
    # Inputs Used
    seed_variety = models.CharField(max_length=100, blank=True, null=True)
    fertilizer_used = models.TextField(blank=True)
    pesticides_used = models.TextField(blank=True)
    
    # Financial
    total_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    total_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    
    # Notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Farming History'
        verbose_name_plural = 'Farming History'
        ordering = ['-year', '-season']
    
    def __str__(self):
        return f"{self.crop_name} - {self.season} {self.year}"
    
    @property
    def profit(self):
        if self.total_revenue and self.total_cost:
            return self.total_revenue - self.total_cost
        return None
    
    @property
    def yield_per_acre(self):
        if self.actual_yield and self.area_planted:
            return self.actual_yield / self.area_planted
        return None


class CreditHistory(models.Model):
    """Farmer credit history for credit scoring"""
    
    farmer_profile = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='credit_history'
    )
    
    loan_type = models.CharField(
        max_length=50,
        choices=[
            ('input', 'Input Financing'),
            ('equipment', 'Equipment Loan'),
            ('seasonal', 'Seasonal Loan'),
            ('insurance', 'Insurance Premium'),
            ('emergency', 'Emergency Loan'),
        ]
    )
    lender_name = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    
    # Dates
    application_date = models.DateField()
    approval_date = models.DateField(blank=True, null=True)
    disbursement_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    repayment_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('disbursed', 'Disbursed'),
            ('active', 'Active'),
            ('repaid', 'Repaid'),
            ('defaulted', 'Defaulted'),
        ],
        default='pending'
    )
    
    # Repayment
    amount_repaid = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    
    # Credit Score Impact
    credit_score_impact = models.IntegerField(default=0)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Credit History'
        verbose_name_plural = 'Credit History'
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.loan_type} - KES {self.loan_amount} ({self.status})"
    
    @property
    def is_fully_repaid(self):
        return self.amount_repaid >= self.loan_amount
    
    @property
    def outstanding_amount(self):
        return self.loan_amount - self.amount_repaid
