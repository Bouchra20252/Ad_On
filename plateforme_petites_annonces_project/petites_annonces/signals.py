from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Advertisement

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a UserProfile instance when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the UserProfile instance when its User is saved"""
    instance.profile.save()

@receiver(post_save, sender=Advertisement)
def set_expiry(sender, instance, created, **kwargs):
    """Set expiry date for new advertisements if not specified"""
    from django.utils import timezone
    import datetime
    
    if created and not instance.expiry_date:
        instance.expiry_date = timezone.now() + datetime.timedelta(days=30)
        instance.save(update_fields=['expiry_date']) 