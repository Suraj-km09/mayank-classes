from rest_framework import serializers
from .models import Course, Subject, Chapter, Batch, BatchEnrollment
from apps.accounts.serializers import UserSerializer

class ChapterSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    materials_count = serializers.IntegerField(source='materials.count', read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'subject', 'title', 'chapter_number', 'description', 'estimated_hours', 'order', 'lessons_count', 'materials_count']

class SubjectSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'course', 'name', 'code', 'icon', 'color_accent', 'order', 'chapters']

class CourseListSerializer(serializers.ModelSerializer):
    subjects_count = serializers.IntegerField(source='subjects.count', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'category', 'short_description', 'target_class',
            'duration_weeks', 'price', 'discount_price', 'thumbnail_url',
            'features', 'is_featured', 'subjects_count'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'category', 'short_description', 'description',
            'target_class', 'duration_weeks', 'price', 'discount_price', 'thumbnail_url',
            'features', 'is_featured', 'order', 'subjects'
        ]

class BatchSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    teachers_list = UserSerializer(source='teachers', many=True, read_only=True)
    enrolled_count = serializers.IntegerField(source='enrollments.count', read_only=True)

    class Meta:
        model = Batch
        fields = [
            'id', 'name', 'code', 'course', 'course_title', 'start_date', 'end_date',
            'schedule_time', 'classroom', 'mode', 'teachers', 'teachers_list',
            'max_capacity', 'enrolled_count'
        ]

class BatchEnrollmentSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    batch_details = BatchSerializer(source='batch', read_only=True)

    class Meta:
        model = BatchEnrollment
        fields = ['id', 'batch', 'student', 'enrollment_date', 'status', 'student_details', 'batch_details']
