from django.contrib import admin
from .models import VideoLesson, VideoProgress, StudyMaterial

@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'subject', 'chapter', 'duration_minutes', 'is_published', 'is_free_preview')
    list_filter = ('course', 'subject', 'is_published', 'is_free_preview')
    search_fields = ('title', 'description')

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'video', 'is_completed', 'watched_duration_seconds', 'last_watched_at')
    list_filter = ('is_completed',)

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'subject', 'material_type', 'file_size_mb', 'download_count')
    list_filter = ('course', 'subject', 'material_type')
    search_fields = ('title', 'description')
