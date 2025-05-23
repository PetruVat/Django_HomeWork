from django.urls import path
from myapp.views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Задачи (Tasks)
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),

    # Подзадачи (SubTasks)
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-retrieve-update-destroy'),
]
