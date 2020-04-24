from rest_framework import serializers
from .models import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('email', 'firstname', 'lastname', 'active', 'staff', 'admin','id','username')
        extra_kwargs = {'user.password': {'write_only': True, 'required': True}}

