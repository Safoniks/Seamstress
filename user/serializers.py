from django.contrib.auth.models import User

from rest_framework import serializers


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

        new_user = validated_data
        password = new_user.pop('password')
        admin_settings = {
            'is_superuser': True,
            'is_staff': True
        }

        if url_name == 'admin':
            new_user.update(admin_settings)

        user = User.objects.create(**new_user)
        user.set_password(password)
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )
        read_only_fields = ('first_name', 'last_name', )
