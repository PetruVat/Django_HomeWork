from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from myapp.models import Category, Task, SubTask
from myapp.serializers import (
    CategorySerializer,
    TaskSerializer,
    SubTaskSerializer,
    UserRegistrationSerializer,
)
from myapp.permissions import IsOwnerOrReadOnly


class CookieTokenObtainPairView(TokenObtainPairView):
    """Return JWT pair in response cookies."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data.get("access")
            refresh = response.data.get("refresh")
            response.set_cookie(
                "access",
                access,
                max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            response.set_cookie(
                "refresh",
                refresh,
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """Refresh JWT pair and update cookies."""

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh") or request.COOKIES.get("refresh")
        if refresh:
            data = request.data.copy()
            data["refresh"] = refresh
            request._full_data = data
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data.get("access")
            refresh_token = response.data.get("refresh", refresh)
            response.set_cookie(
                "access",
                access,
                max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            if refresh_token:
                response.set_cookie(
                    "refresh",
                    refresh_token,
                    max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                )
        return response




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


class RegisterView(APIView):
    """Endpoint for registering new users."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """Blacklist refresh token and remove it from cookies."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('refresh')
        if not token:
            return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(token).blacklist()
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh')
        return response