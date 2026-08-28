from rest_framework import serializers
from .models import VideoLesson, VideoProgress, StudyMaterial
from apps.accounts.serializers import UserSerializer

class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['id', 'student', 'video', 'is_completed', 'watched_duration_seconds', 'last_position_seconds', 'last_watched_at']
        read_only_fields = ['id', 'student', 'last_watched_at']

class VideoLessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name_display', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = VideoLesson
        fields = [
            'id', 'course', 'course_title', 'subject', 'subject_name',
            'chapter', 'chapter_title', 'teacher', 'teacher_name',
            'title', 'description', 'video_url', 'thumbnail_url',
            'duration_minutes', 'order', 'is_published', 'is_free_preview',
            'user_progress'
        ]

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = VideoProgress.objects.filter(student=request.user, video=obj).first()
            if progress:
                return {
                    'is_completed': progress.is_completed,
                    'last_position_seconds': progress.last_position_seconds,
                    'watched_duration_seconds': progress.watched_duration_seconds,
                }
        return {'is_completed': False, 'last_position_seconds': 0, 'watched_duration_seconds': 0}

class StudyMaterialSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name_display', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    material_type_display = serializers.CharField(source='get_material_type_display', read_only=True)

    class Meta:
        model = StudyMaterial
        fields = [
            'id', 'course', 'subject', 'subject_name', 'chapter', 'chapter_title',
            'teacher', 'teacher_name', 'title', 'description', 'material_type',
            'material_type_display', 'file_url', 'file_size_mb', 'download_count',
            'is_published', 'created_at'
        ]
