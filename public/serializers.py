from django.utils import timezone

from rest_framework import serializers

from operation.models import Operation
from worker.models import Worker, Goal
from operationtype.serializers import OperationTypeSerializer
from worker.serializers import WorkerProfileSerializer

from .validators import positive_number, future_date


class MyDateTimeField(serializers.DateTimeField):
    format = '%Y-%m-%d %H:%M:%S'

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(MyDateTimeField, self).to_representation(value)


class WorkerGoalSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(validators=[positive_number])
    start = MyDateTimeField(read_only=True)
    end = MyDateTimeField(validators=[future_date])

    class Meta:
        model = Goal
        fields = (
            'id',
            'name',
            'amount',
            'start',
            'end',
        )


class WorkerDoneDailySerializer(WorkerProfileSerializer):
    done = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'done',
        )

    def get_done(self, obj):
        return obj.daily_done


class RatingDoneDailySerializer(serializers.Serializer):
    my_position = serializers.SerializerMethodField()
    worker_list = serializers.SerializerMethodField()

    def get_my_position(self, obj):
        return obj.get_rating_position_with(prop='daily_done')

    def get_worker_list(self, obj):
        workers = Worker.objects.all_ordered_by(prop='daily_done')
        return WorkerDoneDailySerializer(workers, many=True).data


class PublicWorkerUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, max_length=30)
    last_name = serializers.CharField(write_only=True, max_length=30)

    class Meta:
        model = Worker
        fields = (
            'first_name',
            'last_name',
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

    class Meta:
        model = Operation
        fields = (
            'id',
            'type',
            'product',
        )

    def get_type(self, obj):
        return OperationTypeSerializer(obj.operation_type).data

    def get_product(self, obj):
        return obj.product.name


class PublicOperationDoneSerializer(serializers.Serializer):
    amount = serializers.IntegerField(validators=[positive_number])


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
    daily_salary = serializers.SerializerMethodField()
    last_period_salary = serializers.SerializerMethodField()
    brigade = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()
    operations = serializers.SerializerMethodField()
    timer = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'daily_salary',
            'last_period_salary',
            'brigade',
            'goal',
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
        return obj.daily_salary

    def get_last_period_salary(self, obj):
        return obj.last_period_salary

    def get_goal(self, obj):
        return WorkerGoalSerializer(obj.goal).data

    def get_operations(self, obj):
        return PublicOperationListSerializer(obj.operations, many=True, context={'worker': obj}).data

    def get_timer(self, obj):
        return TimerDetailSerializer(obj).data
