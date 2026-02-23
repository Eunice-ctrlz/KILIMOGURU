from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AdvisoryCategory(models.Model):
    """Categories for advisory content"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Advisory Category'
        verbose_name_plural = 'Advisory Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AdvisoryArticle(models.Model):
    """Agricultural advisory articles"""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('sw', 'Swahili'),
        ('ki', 'Kikuyu'),
        ('lu', 'Luo'),
        ('ka', 'Kalenjin'),
        ('kl', 'Kamba'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    category = models.ForeignKey(
        AdvisoryCategory, on_delete=models.CASCADE, related_name='articles'
    )
    
    # Content
    summary = models.TextField()
    content = models.TextField()
    
    # Media
    featured_image = models.ImageField(upload_to='advisory/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    # Language
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    
    # Related crops
    related_crops = models.ManyToManyField(
        'crops.Crop', blank=True, related_name='advisory_articles'
    )
    
    # Author
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    author_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadata
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Engagement
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Advisory Article'
        verbose_name_plural = 'Advisory Articles'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class Webinar(models.Model):
    """Live webinar sessions"""
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live Now'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Presenter
    presenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='webinars'
    )
    presenter_title = models.CharField(max_length=100, blank=True)
    
    # Schedule
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Platform
    platform = models.CharField(
        max_length=20,
        choices=[
            ('zoom', 'Zoom'),
            ('youtube', 'YouTube Live'),
            ('facebook', 'Facebook Live'),
            ('teams', 'Microsoft Teams'),
        ]
    )
    meeting_link = models.URLField(blank=True, null=True)
    meeting_id = models.CharField(max_length=50, blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    
    # Related topics
    topics = models.JSONField(default=list, blank=True)
    
    # Registration
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    registered_users = models.ManyToManyField(
        User, blank=True, related_name='registered_webinars'
    )
    
    # Recording
    recording_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Webinar'
        verbose_name_plural = 'Webinars'
        ordering = ['-scheduled_date', '-start_time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_full(self):
        if self.max_participants:
            return self.registered_users.count() >= self.max_participants
        return False


class ExpertConsultation(models.Model):
    """One-on-one expert consultations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='consultations'
    )
    expert = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='expert_consultations'
    )
    
    # Topic
    topic = models.CharField(max_length=200)
    description = models.TextField()
    
    # Category
    category = models.ForeignKey(
        AdvisoryCategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    
    # Scheduling
    requested_date = models.DateField(blank=True, null=True)
    requested_time = models.TimeField(blank=True, null=True)
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Communication
    contact_method = models.CharField(
        max_length=20,
        choices=[
            ('phone', 'Phone Call'),
            ('video', 'Video Call'),
            ('chat', 'Chat'),
        ]
    )
    contact_details = models.CharField(max_length=100)
    
    # Consultation notes
    expert_notes = models.TextField(blank=True)
    farmer_feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Expert Consultation'
        verbose_name_plural = 'Expert Consultations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer.username} - {self.topic}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    
    category = models.ForeignKey(
        AdvisoryCategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    
    # Related crops
    related_crops = models.ManyToManyField(
        'crops.Crop', blank=True
    )
    
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-view_count']
    
    def __str__(self):
        return self.question


class FarmingTip(models.Model):
    """Daily farming tips"""
    
    tip = models.TextField()
    
    category = models.ForeignKey(
        AdvisoryCategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    
    # Related crops
    related_crops = models.ManyToManyField(
        'crops.Crop', blank=True
    )
    
    # Schedule
    display_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Farming Tip'
        verbose_name_plural = 'Farming Tips'
        ordering = ['-display_date']
    
    def __str__(self):
        return self.tip[:50] + '...'


class TeleVetConsultation(models.Model):
    """Tele-veterinary consultations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vet_consultations'
    )
    
    # Animal details
    animal_species = models.CharField(max_length=50)
    animal_breed = models.CharField(max_length=100, blank=True)
    animal_age = models.CharField(max_length=50, blank=True)
    
    # Problem
    symptoms = models.TextField()
    duration = models.CharField(max_length=100)
    
    # Images
    image_1 = models.ImageField(upload_to='vet_consultations/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='vet_consultations/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='vet_consultations/', blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Assignment
    assigned_vet = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='assigned_consultations'
    )
    
    # Consultation
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    
    # Follow-up
    follow_up_needed = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tele-Vet Consultation'
        verbose_name_plural = 'Tele-Vet Consultations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer.username} - {self.animal_species} - {self.status}"
