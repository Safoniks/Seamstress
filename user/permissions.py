from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated

from .models import MyUser


class IsAuthenticatedWorker(BasePermission):
    message = 'You must be the worker.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and is_authenticated(request.user) and MyUser.is_worker(user)


class IsAuthenticatedTechnologist(BasePermission):
    message = 'You must be the technologist.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and is_authenticated(request.user) and MyUser.is_technologist(user)


class IsAuthenticatedDirector(BasePermission):
    message = 'You must be the director.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and is_authenticated(request.user) and MyUser.is_director(user)


class IsAuthenticatedDirectorOrTechnologist(BasePermission):
    message = 'You must be the director or technologist.'

    def has_permission(self, request, view):
        user = request.user
        return request.user and is_authenticated(request.user) and MyUser.is_director(user) or MyUser.is_technologist(user)
