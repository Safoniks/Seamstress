from rest_framework import serializers

from .models import OperationTypeCategory


class OperationTypeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationTypeCategory
        fields = (
            'id',
            'name',
            'cost_per_second',
        )
