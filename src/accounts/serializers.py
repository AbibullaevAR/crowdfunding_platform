from rest_framework import serializers

from django.contrib.auth import get_user_model


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')


class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'id', 'is_admin', 'created_at')


class UpdateUserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('is_admin', )
