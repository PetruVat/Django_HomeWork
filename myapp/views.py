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