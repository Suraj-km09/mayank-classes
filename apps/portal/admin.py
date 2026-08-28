from django.contrib import admin
from .models import Notice, Testimonial, SuccessStory, GalleryImage, ContactInquiry

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_role', 'is_pinned', 'published_date')
    list_filter = ('category', 'target_role', 'is_pinned')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'score_or_rank', 'college_admitted', 'year', 'is_featured')
    list_filter = ('year', 'is_featured')

@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'exam_name', 'rank_or_score', 'year', 'is_featured')
    list_filter = ('exam_name', 'year', 'is_featured')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'course_interested', 'status', 'created_at')
    list_filter = ('status', 'course_interested')
    search_fields = ('full_name', 'email', 'phone')
