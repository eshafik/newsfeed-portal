from django.conf import settings
from django.db.models.signals import post_delete, m2m_changed
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F

from app_libs.loggers import log_exception


def many_to_many_data_on_change(sender, instance, **kwargs):
    try:
        if kwargs.get("action") == "post_add" or kwargs.get("action") == "post_remove":
            pass

    except Exception as error_info:
        pass


def update_user_management_on_delete(sender, instance, **kwargs):
    try:
        pass
    except Exception as error_info:
        pass


# post_delete.connect(update_user_management_on_delete, sender=Group)
# m2m_changed.connect(many_to_many_data_on_change, sender=Group.permissions.through)
