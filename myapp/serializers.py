from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers
from myapp.models import Category, Task, SubTask


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
            'is_deleted',
            'deleted_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_deleted', 'deleted_at']


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'categories',
            'status',
            'deadline',
            'created_at',
        ]
        read_only_fields = ['created_at', 'owner']


class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SubTask
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'task',
            'status',
            'deadline',
            'created_at',
        ]
        read_only_fields = ['created_at', 'owner']


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for validating user registration data."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with that username already exists.')
        return value

    def validate_email(self, value):
        # EmailField already checks for valid format but we also ensure uniqueness
        validate_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value