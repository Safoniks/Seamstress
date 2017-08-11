from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated


class IsAuthenticatedWorker(BasePermission):
    message = 'You must be the worker.'

    def has_permission(self, request, view):
        try:
            worker = request.user.worker
        except AttributeError:
            worker = None
        return request.user and is_authenticated(request.user) and worker
