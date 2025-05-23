from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from myapp.models import (
    Task,
    SubTask
)
from myapp.serializers import (
    SubTaskCreateSerializer,
    SubTaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer
)
from django.utils import timezone
from django.db.models import Count
from myapp.pagination import SubTaskPagination



# Create your views here.

def hello(request):
    return HttpResponse("Hello, PETRU!")

# --- Эндпоинт для создания задачи ---
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


# --- Эндпоинт для получения списка задач ---
# class TaskListView(generics.ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


# --- Эндпоинт для получения задачи по ID ---
class TaskDetailView(generics.RetrieveAPIView):
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

class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


# --- Эндпоинт для получения задач по дню недели ---
class TaskListByDayAPIView(APIView):
    def get(self, request):
        day_of_week = request.query_params.get('day_of_week', None)
        if day_of_week:
            tasks = Task.objects.filter(deadline__week_day=self.get_day_number(day_of_week))
        else:
            tasks = Task.objects.all()

        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_day_number(day):
        days = {
            "sunday": 1,
            "monday": 2,
            "tuesday": 3,
            "wednesday": 4,
            "thursday": 5,
            "friday": 6,
            "saturday": 7,
        }
        return days.get(day.lower())


# --- Пагинируемый список подзадач ---
class PaginatedSubTaskListView(generics.ListAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination


# --- Фильтрация подзадач по главной задаче и статусу ---
class FilteredSubTaskListView(generics.ListAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_title = self.request.query_params.get('task', None)
        status = self.request.query_params.get('status', None)

        if task_title and status:
            queryset = queryset.filter(task__title__icontains=task_title, status=status)
        elif task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        elif status:
            queryset = queryset.filter(status=status)

        return queryset
