from django.http import Http404

from rest_framework import serializers

from brigade.models import Brigade
from operation.models import Operation
from public.models import Payroll

from public.validators import positive_number

from .models import Worker, WorkerOperation


class BaseBrigadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brigade
        fields = (
            'id',
            'name',
        )


class CommonOperationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    full_cost = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            'id',
            'name',
            'full_cost',
            'product',
        )

    def get_name(self, obj):
        return obj.operation_type.name

    def get_full_cost(self, obj):
        return obj.operation_type.full_cost

    def get_product(self, obj):
        return obj.product.name


class WorkerListSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    brigade = BaseBrigadeSerializer(read_only=True)
    operations = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'brigade',
            'operations',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_operations(self, obj):
        return CommonOperationSerializer(obj.worker_operations.all(), many=True).data


class WorkerUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, max_length=30)
    last_name = serializers.CharField(write_only=True, max_length=30)

    class Meta:
        model = Worker
        fields = (
            'first_name',
            'last_name',
            'brigade',
        )
        extra_kwargs = {'brigade': {
            'default': None,
            'required': False,
        }}

    def to_representation(self, instance):
        return WorkerListSerializer(instance).data

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.save()
        return super(WorkerUpdateSerializer, self).update(instance, validated_data)


class WorkerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class WorkerOperationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerOperation
        fields = (
            'worker',
            'operation',
        )
        read_only_fields = ('worker',)

    def validate(self, attrs):
        worker = self.context['view'].worker
        operation = attrs.get('operation')
        worker_operation = WorkerOperation.objects.filter(operation=operation, worker=worker)
        if worker_operation.exists():
            raise serializers.ValidationError('Already exist.')
        attrs.update({'worker': worker})
        return attrs


class PayrollCreateSerializer(serializers.Serializer):
    paid = serializers.FloatField(validators=[positive_number])

    def create(self, validated_data):
        worker = self.context['view'].worker
        if not worker:
            raise Http404
        paid = validated_data.get('paid')
        payroll = Payroll(
            worker=worker,
            paid=paid,
            salary=worker.last_period_salary_with_debt,
        )
        payroll.save()

        worker.goal and worker.goal.delete()
        return payroll
