from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academic.models import Course, Subject, Chapter

class VideoLesson(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='video_lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='video_lessons')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_lessons')
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=500, help_text='Direct MP4 URL, YouTube Embed, or Vimeo URL')
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    duration_minutes = models.IntegerField(default=45, help_text='Duration in minutes')
    order = models.IntegerField(default=1)
    is_published = models.BooleanField(default=True)
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['chapter', 'order', 'id']

    def __str__(self):
        return f"{self.course.title} | {self.subject.name} | {self.title}"


class VideoProgress(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(VideoLesson, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    watched_duration_seconds = models.IntegerField(default=0)
    last_position_seconds = models.IntegerField(default=0)
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'video')

    def __str__(self):
        return f"{self.student.username} - {self.video.title} ({'Done' if self.is_completed else 'In Progress'})"


class StudyMaterial(TimeStampedModel):
    MATERIAL_TYPES = [
        ('PDF_NOTES', 'Comprehensive Lecture Notes'),
        ('FORMULA_SHEET', 'Quick Revision Formula Sheet'),
        ('DPP', 'Daily Practice Problems (DPP)'),
        ('PYQ', 'Previous Year Question Bank'),
        ('ASSIGNMENT', 'Class Assignment / Homework'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, related_name='materials')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPES, default='PDF_NOTES')
    file_url = models.URLField(max_length=500, help_text='URL to PDF or cloud storage document')
    file_size_mb = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)
    download_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_material_type_display()}] {self.title}"
