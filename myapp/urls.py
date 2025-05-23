from django.urls import path
from myapp.views import (
    hello,
    TaskListByDayAPIView,
    PaginatedSubTaskListView,
    FilteredSubTaskListView

)


urlpatterns = [
    path('', hello, name='hello'),
    path('tasks/by-day/', TaskListByDayAPIView.as_view(), name='task-list-by-day'),
    path('subtasks/paginated/', PaginatedSubTaskListView.as_view(), name='paginated-subtask-list'),
    path('subtasks/filter/', FilteredSubTaskListView.as_view(), name='filtered-subtask-list'),

]
