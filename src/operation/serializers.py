from rest_framework import serializers

from worker.serializers import WorkerProfileSerializer

from .models import Operation
from operationtype.serializers import OperationTypeSerializer


class ProductOperationListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
    type = serializers.SerializerMethodField()
    workers = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            # 'url',
            'id',
            'type',
            'operation_type',
            'workers',
        )
        extra_kwargs = {'operation_type': {'write_only': True}}

    def get_type(self, obj):
        return OperationTypeSerializer(obj.operation_type).data

    def get_workers(self, obj):
        return WorkerProfileSerializer(obj.worker_set.all(), many=True).data

    def validate_operation_type(self, value):
        product = self.context.get('product')
        operation_type = value

        operation = Operation.objects.filter(product=product, operation_type=operation_type)
        if operation.exists():
            raise serializers.ValidationError('Already exist.')
        return value


class ProductOperationListUpdateSerializer(ProductOperationListSerializer):
    class Meta:
        model = Operation
        fields = (
            'id',
            'type',
            'operation_type',
            'workers',
        )
        extra_kwargs = {'operation_type': {'write_only': True}}

    def validate_operation_type(self, value):
        return value
