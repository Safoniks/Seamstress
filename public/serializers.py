from rest_framework import serializers

from operation.models import Operation
from worker.models import WorkerOperation, Worker
from operationtype.serializers import OperationTypeSerializer

from .validators import positive_number


class PublicOperationListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    done = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            'id',
            'type',
            'product',
            'done',
        )

    def get_type(self, obj):
        return OperationTypeSerializer(obj.operation_type).data

    def get_product(self, obj):
        return obj.product.name

    def get_done(self, obj):
        request = self.context.get('request')
        worker = request.user.worker
        worker_operation = WorkerOperation.objects.get(worker=worker, operation=obj)
        return worker_operation.done


class PublicOperationDoneSerializer(serializers.Serializer):
    amount = serializers.IntegerField(validators=[positive_number])


class PublicWorkerDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    brigade = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'daily_done',
            'daily_salary',
            'goal',
            'brigade',
            'is_active',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_brigade(self, obj):
        return obj.brigade.name


class PublicWorkerUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, max_length=30)
    last_name = serializers.CharField(write_only=True, max_length=30)

    class Meta:
        model = Worker
        fields = (
            'first_name',
            'last_name',
            'goal',
        )

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.save()
        return super(PublicWorkerUpdateSerializer, self).update(instance, validated_data)
