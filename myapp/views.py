from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from myapp.models import Category, Task, SubTask
from myapp.serializers import CategorySerializer, TaskSerializer, SubTaskSerializer
from myapp.permissions import IsOwnerOrReadOnly


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
        task_count = Task.objects.filter(categories=category).count()
        return Response({'category': category.name, 'task_count': task_count})

    def perform_destroy(self, instance):
        """
        Используем мягкое удаление вместо обычного — вызываем кастомный метод `delete`.
        """
        instance.delete()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)