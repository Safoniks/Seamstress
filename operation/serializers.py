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

    def validate_operation_type(self, value):
        view = self.context['view']
        product_id = view.kwargs.get('product_id')
        type_id = value.id

        operation = Operation.objects.filter(product_id=product_id, operation_type_id=type_id)
        if operation:
            raise serializers.ValidationError('Already exist.')
        return value
