from django.contrib import admin
from .models import Course, Subject, Chapter, Batch, BatchEnrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_class', 'price', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'code', 'order')
    list_filter = ('course',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_number', 'title', 'subject', 'estimated_hours')
    list_filter = ('subject__course', 'subject')

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course', 'start_date', 'mode', 'max_capacity')
    list_filter = ('course', 'mode')

@admin.register(BatchEnrollment)
class BatchEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch', 'status', 'enrollment_date')
    list_filter = ('status', 'batch')
