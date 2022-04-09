from .models import File
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserSerializer(ModelSerializer):
    # class Meta:
    #     model = User
    #     fields = ('email','fullname', 'last_login', 'date_joined', 'is_staff')

    #     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'password', 'image', 'approved')
        extra_kwargs = {'password': {'write_only': True}, 'trustworthy': {
            'read_only': True}, 'staff': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "Actual_file", "File_name")
