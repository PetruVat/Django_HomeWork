from rest_framework.pagination import PageNumberPagination


class SubTaskPagination(PageNumberPagination):
    page_size = 5  # Отображение не более 5 подзадач на странице