from django.contrib.auth.backends import ModelBackend

from rest_framework.permissions import BasePermission
from rest_framework import exceptions


class UserPermission(BasePermission, ModelBackend):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        # 'POST': ['%(app_label)s.add_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    authenticated_users_only = True

    def has_perm(self, user_obj, perm, obj=None):
        """
        :param user_obj:
        :param perm:
        :param obj:
        :return:
        """
        return user_obj.is_active and perm in self.get_all_permissions(user_obj, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return any(self.has_perm(obj, perm) for perm in perm_list)

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        """
        :param request:
        :param view:
        :return:
        """
        assert hasattr(view, 'model_name') or getattr(view, 'model_name', None) is not None, (
            'You should define model name inside your API endpoint'
            'e.g.: model_name=<model name> or model_name=None'
        ).format(self.__class__.__name__)

        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (not request.user.is_authenticated and self.authenticated_users_only):
            return False

        if not (request.user.is_blocked or request.user.is_active):
            return False

        if view.model_name:
            perms = self.get_required_permissions(request.method, view.model_name)
            return self.has_perms(perm_list=perms, obj=request.user)
        elif view.model_name is None:
            # for outside service call
            return True
        else:
            return False
