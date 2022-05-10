from .models import File, Student
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'password', 'approved')
        extra_kwargs = {'password': {'write_only': True}, 'trustworthy': {
            'read_only': True}, 'staff': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "Actual_file", "File_name")

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class ListSerializer(serializers.Serializer):
    data= serializers.ListField
