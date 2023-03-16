from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from django.utils.safestring import mark_safe

from .encryption_util import encrypt


# Create your models here.


class PasswordCategory(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    title = models.TextField(
        verbose_name='Title of category'
    )

    class Meta:
        verbose_name = 'Password category'


class UserPassword(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to=PasswordCategory,
        verbose_name='Password category',
        on_delete=models.CASCADE,
    )
    encrypted_password = models.TextField(
        verbose_name='Encrypted password'
    )

    class Meta:
        verbose_name = 'User password'


# method for indicating where to load avatars
def upload_to(instance, filename):
    return 'avatars/%s' % filename


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    secret_key = models.TextField(
        verbose_name='Secret key for decryption'
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
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        secret_key = Fernet.generate_key()
        print(f'{instance}: {secret_key}')
        Profile.objects.create(user=instance, secret_key=encrypt(secret_key))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
