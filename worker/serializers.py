from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Worker
        fields = (
            'id',
            'user',
        )
