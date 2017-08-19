from django.utils import timezone

from rest_framework.serializers import ValidationError


def positive_number(value):
    if value <= 0:
        raise ValidationError('This field must be an positive number.')


def future_date(value):
    if value <= timezone.now():
        raise ValidationError('This field must be an future date.')
