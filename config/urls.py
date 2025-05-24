from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import CategoryViewSet

# Роутер для CategoryViewSet
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Админ панель
    path('admin/', admin.site.urls),

    # Подключение дополнительных маршрутов из приложения (если нужно)
    path('', include('myapp.urls')),

    # Роутер для категорий (включает CRUD и count_tasks)
    path('api/', include(router.urls)),
]
