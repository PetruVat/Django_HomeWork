from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from myapp.views import CategoryViewSet, TaskViewSet, SubTaskViewSet

# Роутеры для Category, Task и SubTask
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')
router.register(r'categories', CategoryViewSet, basename='category')

schema_view = get_schema_view(
    openapi.Info(
        title="API Schema",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT-аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API роуты
    path('api/', include(router.urls)),
]