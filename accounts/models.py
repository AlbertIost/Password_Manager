from django.contrib.auth.models import User
from django.db import models


class ActionLogs(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    action = models.TextField(
        verbose_name='User action'
    )
    note = models.TextField(
        verbose_name='Note for the action',
        null=True
    )
    danger_level = models.PositiveSmallIntegerField(
        verbose_name='The level of danger of the action',
        default=0
    )
    execution_at = models.DateTimeField(
        auto_now_add=True,
        blank=True
    )