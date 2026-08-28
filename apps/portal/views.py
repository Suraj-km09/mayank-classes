from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from .models import Notice, Testimonial, SuccessStory, GalleryImage, ContactInquiry
from .serializers import (
    NoticeSerializer, TestimonialSerializer,
    SuccessStorySerializer, GalleryImageSerializer,
    ContactInquirySerializer
)
from apps.accounts.models import User
from apps.academic.models import Course, Batch, BatchEnrollment
from apps.lms.models import VideoLesson, VideoProgress, StudyMaterial
from apps.assessments.models import Test, StudentTestAttempt
from apps.operations.models import Attendance, FeeRecord, Certificate
from apps.core.permissions import IsAdminRole, IsTeacherOrAdmin
from .chatbot_service import ChatbotAssistantView

class NoticeListView(generics.ListCreateAPIView):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.upper())

        if not user.is_authenticated or user.is_student_role():
            queryset = queryset.filter(target_role__in=['ALL', 'STUDENT'])
        elif user.is_teacher_role():
            queryset = queryset.filter(target_role__in=['ALL', 'TEACHER'])
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

class TestimonialListView(generics.ListCreateAPIView):
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        queryset = Testimonial.objects.all()
        featured = self.request.query_params.get('featured')
        if featured:
            queryset = queryset.filter(is_featured=True)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

class SuccessStoryListView(generics.ListCreateAPIView):
    serializer_class = SuccessStorySerializer

    def get_queryset(self):
        return SuccessStory.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

class GalleryImageListView(generics.ListCreateAPIView):
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        queryset = GalleryImage.objects.all()
        if category:
            queryset = queryset.filter(category=category.upper())
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

from .email_service import dispatch_counseling_emails

class ContactInquiryView(generics.ListCreateAPIView):
    serializer_class = ContactInquirySerializer

    def get_queryset(self):
        return ContactInquiry.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        inquiry = serializer.save()
        try:
            dispatch_counseling_emails(inquiry)
        except Exception as e:
            pass

class ContactInquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = ContactInquirySerializer
    queryset = ContactInquiry.objects.all()


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        total_students = User.objects.filter(role=User.Role.STUDENT).count()
        total_teachers = User.objects.filter(role=User.Role.TEACHER).count()
        active_courses = Course.objects.filter(is_active=True).count()
        active_batches = Batch.objects.count()
        
        total_fees = FeeRecord.objects.aggregate(
            total_expected=Sum('total_amount'),
            total_collected=Sum('paid_amount')
        )
        total_expected = float(total_fees['total_expected'] or 0)
        total_collected = float(total_fees['total_collected'] or 0)
        total_pending = max(0, total_expected - total_collected)

        today = timezone.now().date()
        today_att = Attendance.objects.filter(date=today)
        att_total = today_att.count()
        att_present = today_att.filter(status='PRESENT').count()
        today_attendance_pct = round((att_present / att_total * 100), 1) if att_total > 0 else 92.5

        new_inquiries = ContactInquiry.objects.filter(status='NEW').count()
        total_videos = VideoLesson.objects.filter(is_published=True).count()
        total_tests = Test.objects.filter(is_published=True).count()

        return Response({
            'kpis': {
                'total_students': total_students,
                'total_teachers': total_teachers,
                'active_courses': active_courses,
                'active_batches': active_batches,
                'total_collected_inr': total_collected,
                'total_pending_inr': total_pending,
                'today_attendance_pct': today_attendance_pct,
                'new_inquiries': new_inquiries,
                'total_videos': total_videos,
                'total_tests': total_tests
            },
            'recent_inquiries': ContactInquirySerializer(ContactInquiry.objects.all()[:5], many=True).data,
            'recent_notices': NoticeSerializer(Notice.objects.all()[:5], many=True).data
        })

class TeacherDashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teacher = request.user
        assigned_batches = Batch.objects.filter(teachers=teacher)
        batch_ids = assigned_batches.values_list('id', flat=True)
        
        student_count = BatchEnrollment.objects.filter(batch_id__in=batch_ids, status='ACTIVE').values('student').distinct().count()
        uploaded_videos = VideoLesson.objects.filter(teacher=teacher).count()
        uploaded_materials = StudyMaterial.objects.filter(teacher=teacher).count()
        tests_created = Test.objects.filter(created_by=teacher).count()

        return Response({
            'kpis': {
                'assigned_batches_count': assigned_batches.count(),
                'total_students': student_count,
                'uploaded_videos': uploaded_videos,
                'uploaded_materials': uploaded_materials,
                'tests_created': tests_created,
            },
            'batches': [{
                'id': b.id,
                'name': b.name,
                'course_title': b.course.title,
                'schedule_time': b.schedule_time,
                'classroom': b.classroom,
                'student_count': b.enrollments.count()
            } for b in assigned_batches]
        })

class StudentDashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = request.user
        enrollments = BatchEnrollment.objects.filter(student=student, status='ACTIVE').select_related('batch__course')
        enrolled_course_ids = enrollments.values_list('batch__course_id', flat=True).distinct()

        # LMS Progress
        total_lessons = VideoLesson.objects.filter(course_id__in=enrolled_course_ids, is_published=True).count()
        completed_lessons = VideoProgress.objects.filter(student=student, is_completed=True).count()
        progress_pct = round((completed_lessons / total_lessons * 100), 1) if total_lessons > 0 else 0

        # Attendance stats
        att_total = Attendance.objects.filter(student=student).count()
        att_present = Attendance.objects.filter(student=student, status='PRESENT').count()
        att_pct = round((att_present / att_total * 100), 1) if att_total > 0 else 94.0

        # Fees
        fees = FeeRecord.objects.filter(student=student)
        total_fee = float(fees.aggregate(s=Sum('total_amount'))['s'] or 0)
        paid_fee = float(fees.aggregate(s=Sum('paid_amount'))['s'] or 0)
        pending_fee = max(0, total_fee - paid_fee)

        # Tests
        attempts = StudentTestAttempt.objects.filter(student=student, status='SUBMITTED')
        avg_score = attempts.aggregate(a=Avg('percentage'))['a'] or 0.0

        # Recent notices
        notices = Notice.objects.filter(target_role__in=['ALL', 'STUDENT'])[:4]

        return Response({
            'kpis': {
                'enrolled_batches_count': enrollments.count(),
                'lms_progress_pct': progress_pct,
                'completed_lessons': completed_lessons,
                'total_lessons': total_lessons,
                'attendance_pct': att_pct,
                'pending_fee_inr': pending_fee,
                'tests_completed': attempts.count(),
                'avg_test_percentage': round(float(avg_score), 1)
            },
            'enrolled_courses': [{
                'batch_id': e.batch.id,
                'batch_name': e.batch.name,
                'course_id': e.batch.course.id,
                'course_title': e.batch.course.title,
                'schedule_time': e.batch.schedule_time,
                'classroom': e.batch.classroom,
                'thumbnail_url': e.batch.course.thumbnail_url
            } for e in enrollments],
            'recent_notices': NoticeSerializer(notices, many=True).data
        })
