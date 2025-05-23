from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from myapp.models import Task, SubTask
from myapp.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer, SubTaskSerializer
from myapp.pagination import SubTaskPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone


# --- CRUD для задач (Tasks) ---
# Список задач (с созданием новой задачи)
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']  # Фильтрация по статусу и дедлайну
    search_fields = ['title', 'description']  # Поиск по названию и описанию
    ordering_fields = ['created_at']  # Сортировка по дате создания (по умолчанию DESC)


# Представление для получения, обновления и удаления конкретной задачи
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


# --- Эндпоинт для получения статистики ---
class TaskStatisticsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_count = Task.objects.values('status').annotate(total=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

        response_data = {
            "total_tasks": total_tasks,
            "status_count": list(status_count),
            "overdue_tasks": overdue_tasks
        }

        return Response(response_data, status=status.HTTP_200_OK)

# --- CRUD для подзадач (SubTasks) ---
# Список подзадач (с созданием новой подзадачи)
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']  # Фильтрация по статусу и дедлайну
    search_fields = ['title', 'description']  # Поиск по названию и описанию
    ordering_fields = ['created_at']  # Сортировка по дате создания


# Представление для получения, обновления и удаления конкретной подзадачи
class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
