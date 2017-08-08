from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class IsAuthenticatedWorker(BasePermission):
    message = 'You must be the worker.'

    def has_permission(self, request, view):
        try:
            worker = request.user.worker
        except AttributeError:
            worker = None
        return request.user and is_authenticated(request.user) and worker

    # def has_object_permission(self, request, view, obj):
    #     member = Membership.objects.get(user=request.user)
    #     member.is_active
    #     if request.method in SAFE_METHODS:
    #         return True
    #     return obj.user == request.user