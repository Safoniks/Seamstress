from rest_framework.exceptions import ValidationError

from public.serializers import PublicWorkerDetailSerializer
from user.serializers import UserProfileSerializer
from user.models import MyUser


def jwt_response_payload_handler(token, user=None, request=None):
    url_name = request.resolver_match.url_name

    if url_name == 'login-worker':
        if MyUser.is_worker(user):
            return {
                'token': token,
                'worker': PublicWorkerDetailSerializer(user.worker).data
            }
        raise ValidationError({
            "detail": "Must be a worker."
        })
    elif url_name == 'login-admin':
        if not MyUser.is_worker(user):
            return {
                'token': token,
                'user': UserProfileSerializer(user).data
            }
        raise ValidationError({
            "detail": "Must be an admin."
        })
