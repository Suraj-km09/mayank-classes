from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import User, StudentProfile, TeacherProfile
from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    StudentProfileSerializer, TeacherProfileSerializer
)
from apps.core.permissions import IsAdminRole, IsTeacherOrAdmin

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': f'Welcome back, {user.get_full_name_display()}!'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Registration successful. Welcome to Mayank Classes!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DemoLoginAPIView(APIView):
    """
    Convenience endpoint for prototype reviewers to easily switch roles.
    Supported roles: 'student', 'teacher', 'admin'
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        role = request.data.get('role', 'student').upper()
        if role not in ['ADMIN', 'TEACHER', 'STUDENT']:
            return Response({'error': 'Invalid role requested.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(role=role).first()
        if not user:
            # Fallback if specific role not found
            if role == 'ADMIN':
                user = User.objects.filter(is_superuser=True).first()
        
        if not user:
            return Response({'error': f'No demo user found for role {role}. Please run seed data.'}, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': f'Switched to Demo {role.capitalize()} ({user.get_full_name_display()})'
        })

class StudentListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsTeacherOrAdmin()]
        return [IsAdminRole()]

    def get(self, request):
        students = User.objects.filter(role=User.Role.STUDENT).select_related('student_profile')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        teachers = User.objects.filter(role=User.Role.TEACHER).select_related('teacher_profile')
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)

class UserDetailAPIView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    def delete(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'User removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

