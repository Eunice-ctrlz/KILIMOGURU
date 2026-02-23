from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MarketPrice(models.Model):
    """Real-time market prices from different markets"""
    
    MARKET_CHOICES = [
        ('nairobi', 'Nairobi'),
        ('mombasa', 'Mombasa'),
        ('kisumu', 'Kisumu'),
        ('nakuru', 'Nakuru'),
        ('eldoret', 'Eldoret'),
        ('meru', 'Meru'),
        ('nyeri', 'Nyeri'),
        ('machakos', 'Machakos'),
        ('kisii', 'Kisii'),
        ('kitale', 'Kitale'),
        ('emali', 'Emali'),
        ('kajiado', 'Kajiado'),
    ]
    
    product_name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=[
            ('cereals', 'Cereals'),
            ('legumes', 'Legumes'),
            ('vegetables', 'Vegetables'),
            ('fruits', 'Fruits'),
            ('roots_tubers', 'Roots & Tubers'),
            ('dairy', 'Dairy Products'),
            ('meat', 'Meat & Poultry'),
            ('eggs', 'Eggs'),
            ('other', 'Other'),
        ]
    )
    market = models.CharField(max_length=20, choices=MARKET_CHOICES)
    
    # Price information
    unit = models.CharField(
        max_length=20,
        choices=[
            ('kg', 'Per Kilogram'),
            ('tonne', 'Per Tonne'),
            ('bag_90kg', 'Per 90kg Bag'),
            ('bag_50kg', 'Per 50kg Bag'),
            ('piece', 'Per Piece'),
            ('liter', 'Per Liter'),
            ('crate', 'Per Crate'),
            ('dozen', 'Per Dozen'),
        ]
    )
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Metadata
    price_date = models.DateField()
    source = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Market Price'
        verbose_name_plural = 'Market Prices'
        ordering = ['-price_date', 'product_name']
        unique_together = ['product_name', 'market', 'price_date']
    
    def __str__(self):
        return f"{self.product_name} - {self.get_market_display()} - KES {self.average_price}"


class ProduceListing(models.Model):
    """Farmer produce listings"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    QUALITY_CHOICES = [
        ('premium', 'Premium Grade'),
        ('grade_1', 'Grade 1'),
        ('grade_2', 'Grade 2'),
        ('grade_3', 'Grade 3'),
        ('mixed', 'Mixed Grades'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='produce_listings'
    )
    
    # Product details
    product_name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=MarketPrice.category.field.choices
    )
    variety = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    
    # Quantity and pricing
    quantity_available = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=20, choices=MarketPrice.unit.field.choices)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    
    # Quality
    quality_grade = models.CharField(
        max_length=20, choices=QUALITY_CHOICES, default='grade_1'
    )
    is_organic = models.BooleanField(default=False)
    certifications = models.JSONField(default=list, blank=True)
    
    # Images
    image_1 = models.ImageField(upload_to='produce/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='produce/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='produce/', blank=True, null=True)
    
    # Location
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True, null=True)
    pickup_location = models.TextField()
    
    # Availability
    available_from = models.DateField()
    available_until = models.DateField()
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active'
    )
    
    # Views and inquiries
    view_count = models.PositiveIntegerField(default=0)
    inquiry_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produce Listing'
        verbose_name_plural = 'Produce Listings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity_available} {self.get_unit_display()}"
    
    @property
    def total_value(self):
        return self.quantity_available * self.price_per_unit


class LivestockListing(models.Model):
    """Livestock listings"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='livestock_listings'
    )
    
    # Animal details
    species = models.CharField(
        max_length=20,
        choices=[
            ('cattle', 'Cattle'),
            ('goat', 'Goats'),
            ('sheep', 'Sheep'),
            ('pig', 'Pigs'),
            ('chicken', 'Chicken'),
            ('duck', 'Ducks'),
            ('rabbit', 'Rabbits'),
            ('other', 'Other'),
        ]
    )
    breed = models.CharField(max_length=100)
    age_months = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    
    # Description
    description = models.TextField()
    health_status = models.TextField()
    vaccination_status = models.TextField(blank=True)
    
    # Pricing
    quantity = models.PositiveIntegerField(default=1)
    price_per_animal = models.DecimalField(max_digits=12, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    
    # Images
    image_1 = models.ImageField(upload_to='livestock/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='livestock/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='livestock/', blank=True, null=True)
    
    # Location
    county = models.CharField(max_length=50)
    pickup_location = models.TextField()
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Livestock Listing'
        verbose_name_plural = 'Livestock Listings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_species_display()} - {self.breed} - KES {self.price_per_animal}"


class BuyerInquiry(models.Model):
    """Buyer inquiries for listings"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    listing = models.ForeignKey(
        ProduceListing, on_delete=models.CASCADE, related_name='inquiries'
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer_inquiries'
    )
    
    # Inquiry details
    quantity_requested = models.DecimalField(max_digits=12, decimal_places=2)
    proposed_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    message = models.TextField()
    
    # Contact
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    
    # Response
    farmer_response = models.TextField(blank=True)
    response_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Buyer Inquiry'
        verbose_name_plural = 'Buyer Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Inquiry for {self.listing.product_name} by {self.buyer.username}"


class BuyerRequest(models.Model):
    """Buyer requests for produce"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer_requests'
    )
    
    # Request details
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=MarketPrice.category.field.choices)
    quantity_required = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=20, choices=MarketPrice.unit.field.choices)
    
    # Pricing
    max_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Quality requirements
    quality_grade = models.CharField(
        max_length=20, choices=ProduceListing.quality_grade.field.choices, blank=True
    )
    requires_organic = models.BooleanField(default=False)
    
    # Location preference
    preferred_counties = models.JSONField(default=list, blank=True)
    
    # Timeline
    required_by_date = models.DateField()
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active'
    )
    
    # Contact
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Buyer Request'
        verbose_name_plural = 'Buyer Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.buyer.username} wants {self.quantity_required} {self.unit} of {self.product_name}"


class Transaction(models.Model):
    """Completed transactions"""
    
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Parties
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sales'
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases'
    )
    
    # Product details
    product_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Transaction details
    transaction_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_location = models.TextField()
    
    # Payment
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default='mpesa'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('partial', 'Partial'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    
    # Ratings
    farmer_rating = models.PositiveIntegerField(blank=True, null=True)
    buyer_rating = models.PositiveIntegerField(blank=True, null=True)
    farmer_review = models.TextField(blank=True)
    buyer_review = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.product_name} - {self.farmer.username} to {self.buyer.username}"
