from django.urls import path
from .views import (
    CourseListView, CourseDetailView,
    SubjectListView, ChapterListView,
    BatchListView, BatchEnrollmentView
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='api-courses'),
    path('courses/<int:id>/', CourseDetailView.as_view(), name='api-course-detail'),
    path('subjects/', SubjectListView.as_view(), name='api-subjects'),
    path('chapters/', ChapterListView.as_view(), name='api-chapters'),
    path('batches/', BatchListView.as_view(), name='api-batches'),
    path('enrollments/', BatchEnrollmentView.as_view(), name='api-enrollments'),
]
