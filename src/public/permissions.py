from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated

from user.models import MyUser


class IsActiveWorker(BasePermission):
    message = 'The worker is not working now.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and MyUser.is_worker(user) and user.worker.is_active


class IsNotActiveWorker(BasePermission):
    message = 'The worker is working now.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and MyUser.is_worker(user) and not user.worker.is_active