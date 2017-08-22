from rest_framework import serializers

from operationtypecategory.serializers import OperationTypeCategorySerializer

from .models import OperationType


class OperationTypeSerializer(serializers.ModelSerializer):
    category = OperationTypeCategorySerializer(read_only=True)
    category_id = serializers.ModelField(model_field=OperationType()._meta.get_field('category'), write_only=True)

    class Meta:
        model = OperationType
        fields = (
            'id',
            'name',
            'category',
            'category_id',
            'duration',
            'full_cost',
        )
        read_only_fields = ('full_cost',)
