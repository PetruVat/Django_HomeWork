from rest_framework import serializers
from myapp.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'is_deleted', 'deleted_at']
        read_only_fields = ['created_at', 'updated_at', 'is_deleted', 'deleted_at']
