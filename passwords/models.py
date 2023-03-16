from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
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


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    secret_key = models.TextField(
        verbose_name='Secret key for decryption'
    )

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
