from rest_framework import serializers

from brigade.models import Brigade

from .models import Worker


class BaseBrigadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brigade
        fields = (
            'id',
            'name',
        )


class WorkerListSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    brigade = BaseBrigadeSerializer(read_only=True)
    brigade_id = serializers.ModelField(model_field=Worker()._meta.get_field('brigade'), write_only=True)

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'brigade',
            'brigade_id',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


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
