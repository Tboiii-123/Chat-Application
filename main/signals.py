from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile,Friend

@receiver(post_save, sender=Profile)
def create_friend_for_profile(sender, instance, created, **kwargs):
    if created:  # Check if this is a new Profile instance
        Friend.objects.create(profile=instance)
