from rest_framework import serializers
from .models import Notice, Testimonial, SuccessStory, GalleryImage, ContactInquiry

class NoticeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'category', 'category_display', 'target_role',
            'content', 'is_pinned', 'published_date', 'attachment_url', 'created_at'
        ]

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'student_name', 'course_name', 'score_or_rank',
            'college_admitted', 'review_text', 'rating', 'avatar_url',
            'year', 'is_featured'
        ]

class SuccessStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessStory
        fields = [
            'id', 'student_name', 'exam_name', 'rank_or_score',
            'image_url', 'summary', 'story', 'year', 'is_featured'
        ]

class GalleryImageSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'category', 'category_display', 'image_url', 'caption']

class ContactInquirySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ContactInquiry
        fields = [
            'id', 'full_name', 'email', 'phone', 'course_interested',
            'current_class', 'message', 'status', 'status_display',
            'notes', 'created_at'
        ]
