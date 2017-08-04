from rest_framework import serializers

from .models import Brigade


class BrigadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brigade
        fields = (
            'id',
            'name',
        )
