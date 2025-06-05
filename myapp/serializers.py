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
            'id',
            'owner',
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