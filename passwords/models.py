from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


# Create your models here.
class UserPassword(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    website_password = models.TextField(
        verbose_name='Website password'
    )
    website_name = models.TextField(
        verbose_name='Name of website',
        null=True
    )
    website_link = models.TextField(
        verbose_name='URL to website',
        null=True
    )
    website_username = models.TextField(
        verbose_name='Login on the website',
        null=True
    )
    website_notes = models.TextField(
        verbose_name='Website notes',
        null=True
    )

    class Meta:
        verbose_name = 'User password'


# method for indicating where to load avatars
def upload_to(instance, filename):
    return f'avatars/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    master_password = models.TextField(
        verbose_name='Master password',
        null=True
    )


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # for profile that created from python manage.py createsuperuser
        if profile.master_password is None:
            profile.master_password = profile.user.password
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
