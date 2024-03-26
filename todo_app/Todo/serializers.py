from rest_framework import serializers

from . import models

# Serializers goes here


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username")
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance


# Todo Serializer
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = "__all__"
        read_only_fields = ["user"]
