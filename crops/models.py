from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Crop(models.Model):
    """Crop database with planting information"""
    
    CROP_CATEGORIES = [
        ('cereals', 'Cereals'),
        ('legumes', 'Legumes'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('roots_tubers', 'Roots & Tubers'),
        ('cash_crops', 'Cash Crops'),
        ('fodder', 'Fodder Crops'),
        ('herbs', 'Herbs & Spices'),
    ]
    
    name = models.CharField(max_length=100)
    local_name = models.CharField(max_length=100, blank=True, null=True)
    scientific_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CROP_CATEGORIES)
    
    # Growing conditions
    optimal_temperature_min = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    optimal_temperature_max = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    rainfall_requirement_min = models.DecimalField(
        max_digits=6, decimal_places=1, blank=True, null=True
    )
    rainfall_requirement_max = models.DecimalField(
        max_digits=6, decimal_places=1, blank=True, null=True
    )
    growing_period_days = models.PositiveIntegerField(blank=True, null=True)
    
    # Planting calendar for Kenya
    planting_months_short_rains = models.CharField(
        max_length=50, 
        default='Oct,Nov',
        help_text="Months for short rains planting"
    )
    planting_months_long_rains = models.CharField(
        max_length=50,
        default='Mar,Apr',
        help_text="Months for long rains planting"
    )
    
    # Soil requirements
    preferred_soil_types = models.JSONField(default=list, blank=True)
    preferred_ph_min = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True
    )
    preferred_ph_max = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True
    )
    
    # Economic info
    average_yield_per_acre = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_price_per_kg = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Crop'
        verbose_name_plural = 'Crops'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CropVariety(models.Model):
    """Specific crop varieties"""
    
    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, related_name='varieties'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Characteristics
    is_drought_resistant = models.BooleanField(default=False)
    is_disease_resistant = models.BooleanField(default=False)
    is_high_yielding = models.BooleanField(default=False)
    is_early_maturing = models.BooleanField(default=False)
    
    # Seed information
    seed_rate_per_acre = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    seed_rate_unit = models.CharField(
        max_length=20,
        choices=[
            ('kg', 'Kilograms'),
            ('g', 'Grams'),
        ],
        default='kg'
    )
    
    # Certified by
    certifying_body = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Crop Variety'
        verbose_name_plural = 'Crop Varieties'
        ordering = ['crop__name', 'name']
    
    def __str__(self):
        return f"{self.crop.name} - {self.name}"


class FarmerCrop(models.Model):
    """Crops planted by farmers"""
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('planted', 'Planted'),
        ('germinating', 'Germinating'),
        ('vegetative', 'Vegetative Growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting/Grain Filling'),
        ('mature', 'Ready for Harvest'),
        ('harvested', 'Harvested'),
        ('failed', 'Failed/Crop Loss'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='crops'
    )
    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, related_name='farmer_crops'
    )
    variety = models.ForeignKey(
        CropVariety, on_delete=models.SET_NULL, blank=True, null=True
    )
    parcel = models.ForeignKey(
        'farmers.FarmParcel', on_delete=models.SET_NULL, blank=True, null=True
    )
    
    # Planting details
    season = models.CharField(
        max_length=20,
        choices=[
            ('short_rains', 'Short Rains'),
            ('long_rains', 'Long Rains'),
            ('dry_season', 'Dry Season'),
        ]
    )
    year = models.PositiveIntegerField()
    planting_date = models.DateField()
    expected_harvest_date = models.DateField(blank=True, null=True)
    actual_harvest_date = models.DateField(blank=True, null=True)
    
    # Area and density
    area_planted = models.DecimalField(max_digits=10, decimal_places=2)
    planting_density = models.CharField(max_length=50, blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='planned'
    )
    
    # Inputs used
    seed_quantity_used = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    fertilizers_applied = models.JSONField(default=dict, blank=True)
    pesticides_applied = models.JSONField(default=dict, blank=True)
    
    # Yield
    expected_yield = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    actual_yield = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
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
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Farmer Crop'
        verbose_name_plural = 'Farmer Crops'
        ordering = ['-planting_date']
    
    def __str__(self):
        return f"{self.crop.name} - {self.season} {self.year}"


class PestDisease(models.Model):
    """Pest and disease database"""
    
    TYPE_CHOICES = [
        ('pest', 'Pest'),
        ('disease', 'Disease'),
        ('weed', 'Weed'),
        ('deficiency', 'Nutrient Deficiency'),
    ]
    
    name = models.CharField(max_length=100)
    local_name = models.CharField(max_length=100, blank=True, null=True)
    scientific_name = models.CharField(max_length=100, blank=True, null=True)
    pest_disease_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Affected crops
    affected_crops = models.ManyToManyField(Crop, related_name='pests_diseases')
    
    # Identification
    symptoms = models.TextField(help_text="Description of symptoms")
    image = models.ImageField(upload_to='pests_diseases/', blank=True, null=True)
    
    # Control methods
    chemical_control = models.TextField(blank=True)
    organic_control = models.TextField(blank=True)
    preventive_measures = models.TextField(blank=True)
    
    # Severity
    severity_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ]
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Pest/Disease'
        verbose_name_plural = 'Pests & Diseases'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PestDiseaseDetection(models.Model):
    """AI-based pest/disease detection records"""
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='detections'
    )
    image = models.ImageField(upload_to='detections/')
    
    # Detection results
    detected_pest_disease = models.ForeignKey(
        PestDisease, on_delete=models.SET_NULL, blank=True, null=True
    )
    confidence_score = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    ai_suggestions = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='verified_detections'
    )
    expert_notes = models.TextField(blank=True)
    
    # Location
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pest/Disease Detection'
        verbose_name_plural = 'Pest/Disease Detections'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Detection by {self.farmer.username} on {self.created_at.date()}"


class Livestock(models.Model):
    """Livestock management"""
    
    SPECIES_CHOICES = [
        ('cattle', 'Cattle'),
        ('goat', 'Goats'),
        ('sheep', 'Sheep'),
        ('pig', 'Pigs'),
        ('chicken', 'Chicken'),
        ('duck', 'Ducks'),
        ('rabbit', 'Rabbits'),
        ('bee', 'Bees'),
        ('fish', 'Fish'),
        ('other', 'Other'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='livestock'
    )
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    
    # Identification
    tag_number = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    
    # Details
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )
    date_of_birth = models.DateField(blank=True, null=True)
    date_acquired = models.DateField(blank=True, null=True)
    acquisition_method = models.CharField(
        max_length=20,
        choices=[
            ('born', 'Born on Farm'),
            ('purchased', 'Purchased'),
            ('gift', 'Gift'),
            ('inheritance', 'Inheritance'),
        ],
        blank=True, null=True
    )
    
    # Health
    is_healthy = models.BooleanField(default=True)
    health_notes = models.TextField(blank=True)
    vaccination_records = models.JSONField(default=dict, blank=True)
    
    # Production
    is_for_breeding = models.BooleanField(default=True)
    is_for_meat = models.BooleanField(default=False)
    is_for_milk = models.BooleanField(default=False)
    is_for_eggs = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    date_sold = models.DateField(blank=True, null=True)
    sale_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Livestock'
        verbose_name_plural = 'Livestock'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_species_display()} - {self.name or self.tag_number or 'Unnamed'}"
    
    @property
    def age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return (today - self.date_of_birth).days // 365
        return None


class LivestockProduction(models.Model):
    """Livestock production records"""
    
    livestock = models.ForeignKey(
        Livestock, on_delete=models.CASCADE, related_name='production_records'
    )
    production_date = models.DateField()
    
    # Production type
    production_type = models.CharField(
        max_length=20,
        choices=[
            ('milk', 'Milk'),
            ('eggs', 'Eggs'),
            ('wool', 'Wool'),
            ('manure', 'Manure'),
        ]
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    
    # Value
    market_value = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Livestock Production'
        verbose_name_plural = 'Livestock Production Records'
        ordering = ['-production_date']
    
    def __str__(self):
        return f"{self.livestock} - {self.production_type} on {self.production_date}"


class PlantingCalendar(models.Model):
    """Planting calendar for Kenya regions"""
    
    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, related_name='planting_calendars'
    )
    region = models.CharField(max_length=100)
    
    # Planting windows
    short_rains_start = models.PositiveIntegerField(
        help_text="Start month (1-12)"
    )
    short_rains_end = models.PositiveIntegerField(
        help_text="End month (1-12)"
    )
    long_rains_start = models.PositiveIntegerField(
        help_text="Start month (1-12)"
    )
    long_rains_end = models.PositiveIntegerField(
        help_text="End month (1-12)"
    )
    
    # Activities
    land_preparation = models.TextField(blank=True)
    planting_activities = models.TextField(blank=True)
    weeding_schedule = models.TextField(blank=True)
    fertilization_schedule = models.TextField(blank=True)
    pest_control = models.TextField(blank=True)
    harvest_window = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Planting Calendar'
        verbose_name_plural = 'Planting Calendars'
        unique_together = ['crop', 'region']
    
    def __str__(self):
        return f"{self.crop.name} - {self.region}"
