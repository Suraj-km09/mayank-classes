from django.urls import path
from .views import (
    VideoLessonListView, VideoLessonDetailView,
    VideoProgressUpdateView, StudyMaterialListView,
    CourseCurriculumView
)

urlpatterns = [
    path('videos/', VideoLessonListView.as_view(), name='api-videos'),
    path('videos/<int:id>/', VideoLessonDetailView.as_view(), name='api-video-detail'),
    path('videos/<int:video_id>/progress/', VideoProgressUpdateView.as_view(), name='api-video-progress'),
    path('study-materials/', StudyMaterialListView.as_view(), name='api-study-materials'),
    path('courses/<int:course_id>/curriculum/', CourseCurriculumView.as_view(), name='api-course-curriculum'),
]
