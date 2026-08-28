from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course, Subject, Chapter, Batch, BatchEnrollment
from .serializers import (
    CourseListSerializer, CourseDetailSerializer,
    SubjectSerializer, ChapterSerializer,
    BatchSerializer, BatchEnrollmentSerializer
)
from apps.core.permissions import IsTeacherOrAdmin, IsAdminRole

class CourseListView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')
        if category:
            queryset = queryset.filter(category=category.upper())
        if featured:
            queryset = queryset.filter(is_featured=True)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.filter(is_active=True)
    lookup_field = 'id'

    def get_serializer_class(self):
        return CourseDetailSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminRole()]
        return [permissions.AllowAny()]

class SubjectListView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        queryset = Subject.objects.filter(is_active=True)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

class ChapterListView(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        queryset = Chapter.objects.filter(is_active=True)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

class BatchListView(generics.ListCreateAPIView):
    serializer_class = BatchSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Batch.objects.none()
        
        if user.is_admin_role():
            return Batch.objects.all()
        elif user.is_teacher_role():
            return Batch.objects.filter(teachers=user)
        else:
            return Batch.objects.filter(enrollments__student=user, enrollments__status='ACTIVE')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

class BatchEnrollmentView(generics.ListCreateAPIView):
    serializer_class = BatchEnrollmentSerializer

    def get_queryset(self):
        batch_id = self.request.query_params.get('batch_id')
        user = self.request.user
        if not user.is_authenticated:
            return BatchEnrollment.objects.none()
        
        queryset = BatchEnrollment.objects.all()
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        
        if user.is_student_role():
            queryset = queryset.filter(student=user)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]
