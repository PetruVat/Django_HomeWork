from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.models import Category, Task
from myapp.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet для модели Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        """
        Кастомный метод для подсчета количества задач в категории.
        """
        category = self.get_object()
        task_count = Task.objects.filter(category=category, is_deleted=False).count()
        return Response({'category': category.name, 'task_count': task_count})

    def perform_destroy(self, instance):
        """
        Используем мягкое удаление вместо обычного — вызываем кастомный метод `delete`.
        """
        instance.delete()
