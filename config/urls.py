from django.contrib import admin
from django.urls import path, include
from myapp.views import (
    TaskListCreateView,  # Импорт вместо TaskCreateView
    TaskRetrieveUpdateDestroyView,  # Этот заменяет TaskDetailView
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,  # Этот заменяет SubTaskDetailUpdateDeleteView
)

urlpatterns = [
    # Админ панель
    path('admin/', admin.site.urls),

    # Подключение маршрутов приложения "myapp"
    path('', include('myapp.urls')),

    # Маршруты для задач
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # Исправлено
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    # Исправлено
    path('api/tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),

    # Маршруты для подзадач
    path('api/subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-retrieve-update-destroy'),
    # Исправлено
]
