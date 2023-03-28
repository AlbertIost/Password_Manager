from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from passwords.models import Profile
from passwords.utils import get_client_ip

class ActionLog(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        verbose_name='Profile',
        on_delete=models.CASCADE,
    )
    action = models.TextField(
        verbose_name='User action'
    )
    note = models.TextField(
        verbose_name='Note for the action',
        null=True
    )
    ip_address = models.TextField(
        verbose_name='IP address from which the action was performed'
    )
    danger_level = models.PositiveSmallIntegerField(
        verbose_name='The level of danger of the action',
        default=0
    )
    execution_at = models.DateTimeField(
        auto_now_add=True,
        blank=True
    )


@receiver(user_logged_in, sender=User)
def user_logged_in_action_log(sender, request, user, **kwargs):
    ActionLog.objects.create(
        profile=user.profile,
        action='Logged in',
        ip_address=get_client_ip(request)
    )


@receiver(user_logged_out, sender=User)
def user_logged_out_action_log(sender, request, user, **kwargs):
    ActionLog.objects.create(
        profile=user.profile,
        action='Logged out',
        ip_address=get_client_ip(request)
    )


@receiver(user_login_failed)
def user_login_failed_action_log(sender, credentials, request, **kwargs):
    try:
        profile = Profile.objects.get(user__username=credentials['username'])
        ActionLog.objects.create(
            profile=profile,
            action='Failed to log in',
            ip_address=get_client_ip(request)
        )
    except ObjectDoesNotExist:
        pass
