import jwt

from django.utils import timezone
from django.conf import settings

from rest_framework.exceptions import ValidationError

from public.serializers import PublicWorkerDetailSerializer
from user.serializers import UserProfileSerializer
from user.models import MyUser


def jwt_payload_handler(user):
    return {
        'user_id': user.pk,
        'username': user.username,
        'scope': MyUser.get_scope(user),
        'exp': timezone.now() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
    }


def jwt_response_payload_handler(token, user=None, request=None):
    url_name = request.resolver_match.url_name

    if url_name == 'login-worker':
        if MyUser.is_worker(user):
            return {
                'token': token,
                'worker': PublicWorkerDetailSerializer(user.worker).data,
                'scope': MyUser.get_scope(user),
            }
        raise ValidationError({
            "detail": "Must be a worker."
        })
    elif url_name == 'login-admin':
        if MyUser.is_director(user) or MyUser.is_technologist(user):
            return {
                'token': token,
                'user': UserProfileSerializer(user).data,
                'scope': MyUser.get_scope(user),
            }
        raise ValidationError({
            "detail": "Must be an admin."
        })


def create_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')
