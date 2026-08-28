from rest_framework import serializers
from .models import Attendance, FeeRecord, Certificate
from apps.accounts.serializers import UserSerializer
from apps.academic.serializers import BatchSerializer, CourseListSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name_display', read_only=True)
    roll_number = serializers.CharField(source='student.student_profile.roll_number', read_only=True, default='')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'batch', 'student', 'student_name', 'roll_number',
            'date', 'status', 'status_display', 'marked_by', 'remarks'
        ]

class FeeRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name_display', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    roll_number = serializers.CharField(source='student.student_profile.roll_number', read_only=True, default='')
    course_title = serializers.CharField(source='course.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    due_amount = serializers.ReadOnlyField()

    class Meta:
        model = FeeRecord
        fields = [
            'id', 'student', 'student_name', 'student_email', 'roll_number',
            'course', 'course_title', 'batch', 'invoice_number', 'title',
            'total_amount', 'paid_amount', 'due_amount', 'due_date', 'status',
            'status_display', 'payment_mode', 'payment_date', 'transaction_id',
            'receipt_url', 'remarks'
        ]

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name_display', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'certificate_number', 'title', 'issue_date', 'grade',
            'verification_code', 'description', 'certificate_url'
        ]
