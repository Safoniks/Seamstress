from rest_framework import serializers

from .models import OperationType


class OperationTypeSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="operation-type:operation-type-detail")

    class Meta:
        model = OperationType
        fields = (
            # 'url',
            'id',
            'name',
            'duration',
            'cost_per_second',
            'full_cost',
        )
        read_only_fields = ('full_cost',)


