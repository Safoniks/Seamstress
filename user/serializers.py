from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import serializers

from public.validators import positive_number

from user.models import MyUser


class WorkerCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        worker = MyUser.objects.create_worker(**validated_data)
        return worker


class TechnologistCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        technologist = MyUser.objects.create_technologist(**validated_data)
        return technologist


class DirectorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        director = MyUser.objects.create_director(**validated_data)
        return director


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        read_only_fields = ('first_name', 'last_name', 'email')


class SettingsSerializer(serializers.Serializer):
    salary_days = serializers.IntegerField(validators=[positive_number])
    working_days = serializers.IntegerField(validators=[positive_number])
    working_hours = serializers.IntegerField(validators=[positive_number])

    def create(self, validated_data):
        settings.APPLICATION_SETTINGS = validated_data
        return validated_data
