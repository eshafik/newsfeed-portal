from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.user.models import User


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    country = ArrayField(models.CharField(max_length=45), default=list)
    source = ArrayField(models.CharField(max_length=255), default=list)
    keywords = ArrayField(models.CharField(max_length=45), default=list)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_preference'
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'
