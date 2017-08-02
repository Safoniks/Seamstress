from rest_framework import serializers

from .models import Operation
from operationtype.serializers import OperationTypeSerializer


class ProductOperationListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
    type = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            # 'url',
            'id',
            'type',
            'operation_type',
        )
        extra_kwargs = {'operation_type': {'write_only': True}}

    def get_type(self, obj):
        return OperationTypeSerializer(obj.operation_type).data
