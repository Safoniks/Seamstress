from django.utils import timezone

from rest_framework import serializers

from operation.models import Operation
from worker.models import Worker
from operationtype.serializers import OperationTypeSerializer

from .validators import positive_number


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
        worker = request.user.worker if request else self.context.get('worker')
        return worker.get_all_done(operation=obj)


class PublicOperationDoneSerializer(serializers.Serializer):
    amount = serializers.IntegerField(validators=[positive_number])


class MyDateTimeField(serializers.DateTimeField):
    format = '%Y-%m-%d %H:%M:%S'

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(MyDateTimeField, self).to_representation(value)


class TimerDetailSerializer(serializers.ModelSerializer):
    time_worked = serializers.DurationField(source='daily_time_worked')
    last_reset = MyDateTimeField()

    class Meta:
        model = Worker
        fields = (
            'is_working',
            'time_worked',
            'last_reset',
        )
        read_only_fields = (
            'is_working',
            'time_worked',
            'last_reset',
        )


class PublicWorkerDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    brigade = serializers.SerializerMethodField()
    operations = serializers.SerializerMethodField()
    daily_salary = serializers.SerializerMethodField()
    period_salary = serializers.SerializerMethodField()
    timer = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'daily_salary',
            'period_salary',
            'goal',
            'brigade',
            'operations',
            'timer',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_brigade(self, obj):
        return obj.brigade_name

    def get_daily_salary(self, obj):
        return obj.get_daily_done(field='cost')

    def get_period_salary(self, obj):
        return obj.get_period_done(field='cost')

    def get_operations(self, obj):
        return PublicOperationListSerializer(obj.operations, many=True, context={'worker': obj}).data

    def get_timer(self, obj):
        return TimerDetailSerializer(obj).data
