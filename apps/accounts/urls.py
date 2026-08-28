from django.urls import path
from .views import (
    LoginAPIView, LogoutAPIView, MeAPIView,
    RegisterAPIView, DemoLoginAPIView,
    StudentListAPIView, TeacherListAPIView,
    UserDetailAPIView
)

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/me/', MeAPIView.as_view(), name='api-me'),
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/demo-login/', DemoLoginAPIView.as_view(), name='api-demo-login'),
    path('students/', StudentListAPIView.as_view(), name='api-students-list'),
    path('teachers/', TeacherListAPIView.as_view(), name='api-teachers-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='api-user-detail'),
]
