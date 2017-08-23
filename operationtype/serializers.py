from rest_framework import serializers

from operationtypecategory.serializers import OperationTypeCategorySerializer

from .models import OperationType


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = (
            'id',
            'name',
            'category',
            'duration',
            'full_cost',
        )
        read_only_fields = ('full_cost',)

    def to_representation(self, instance):
        ret = super(OperationTypeSerializer, self).to_representation(instance)
        ret['category'] = OperationTypeCategorySerializer(instance.category).data
        return ret
