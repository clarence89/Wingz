# serializers.py
from rest_framework import serializers
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "description")


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(default=None, required=False, read_only=True)

    class Meta:
        model = User
        exclude = ("password",)
