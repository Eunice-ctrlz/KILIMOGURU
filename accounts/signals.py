from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email when a new user is created"""
    if created and instance.email:
        try:
            send_mail(
                subject='Welcome to KILIMO GURU!',
                message=f'''
                Dear {instance.get_full_name() or instance.username},
                
                Welcome to KILIMO GURU - Your Smart Agriculture Partner!
                
                We're excited to have you join our community of farmers and agricultural enthusiasts.
                
                With KILIMO GURU, you can:
                - Access real-time weather forecasts and alerts
                - Manage your crops and livestock effectively
                - Connect with buyers and get fair market prices
                - Purchase verified agricultural inputs
                - Access M-Pesa integrated financial services
                - Learn from agricultural experts
                
                Get started by completing your profile and exploring our features.
                
                Best regards,
                The KILIMO GURU Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        except Exception as e:
            # Log the error but don't break the registration flow
            print(f"Failed to send welcome email: {e}")


@receiver(post_save, sender=User)
def create_farmer_profile(sender, instance, created, **kwargs):
    """Create farmer profile when a new farmer user is created"""
    if created and instance.is_farmer:
        from farmers.models import FarmerProfile
        FarmerProfile.objects.get_or_create(
            user=instance,
            defaults={
                'farm_size': 0,
                'farm_location': instance.county or '',
            }
        )
