from django.contrib.auth.models import User

from rest_framework import serializers

from user.models import MyUser


class UserCreateSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        url_name = request.resolver_match.url_name

        if url_name == 'register-admin':
            user = MyUser.objects.create_admin(**validated_data)
        else:
            user = MyUser.objects.create_worker(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )
        read_only_fields = ('first_name', 'last_name', )
