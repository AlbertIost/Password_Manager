from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
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
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to=upload_to,
        null=True,
        blank=True
    )

    def get_avatar(self):
        if not self.avatar:
            return '/static/images/avatar.svg'
        return self.avatar.url

    # method to create a fake table field in read only mode
    def avatar_tag(self):
        return mark_safe(f'<img src="{self.get_avatar()}" width="50" height="50" />')

    avatar_tag.short_description = 'Avatar'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


