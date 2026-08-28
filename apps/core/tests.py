from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.academic.models import Course, Subject, Chapter, Batch, BatchEnrollment
from apps.lms.models import VideoLesson, VideoProgress
from apps.assessments.models import Test, Question, StudentTestAttempt
from apps.operations.models import Attendance, FeeRecord, Certificate
from apps.portal.models import ContactInquiry

class PlatformSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Admin user
        self.admin = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='testpassword123',
            role=User.Role.ADMIN
        )

        # Teacher user
        self.teacher = User.objects.create_user(
            username='teacher_test',
            email='teacher@test.com',
            password='testpassword123',
            role=User.Role.TEACHER
        )

        # Student user
        self.student = User.objects.create_user(
            username='student_test',
            email='student@test.com',
            password='testpassword123',
            role=User.Role.STUDENT
        )

        # Create Course hierarchy
        self.course = Course.objects.create(
            title='JEE Advanced Test Course',
            slug='jee-test-course',
            category='ENGINEERING',
            target_class='Class 11 & 12',
            price=50000.00
        )
        self.subject = Subject.objects.create(
            course=self.course,
            name='Physics Test',
            code='PHY-TEST'
        )
        self.chapter = Chapter.objects.create(
            subject=self.subject,
            title='Kinematics Test',
            chapter_number=1
        )
        self.lesson = VideoLesson.objects.create(
            course=self.course,
            subject=self.subject,
            chapter=self.chapter,
            title='Lesson 1: Projectile Motion',
            video_url='https://www.youtube.com/embed/test',
            duration_minutes=45
        )

    def test_01_authentication_login(self):
        """Test API Login endpoint"""
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'student_test',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'student_test')

    def test_02_demo_login(self):
        """Test 1-click Demo Login endpoint"""
        response = self.client.post('/api/auth/demo-login/', {'role': 'student'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['role'], 'STUDENT')

    def test_03_courses_and_curriculum_api(self):
        """Test Course list and hierarchical curriculum"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results'] if 'results' in response.data else response.data), 1)

        curriculum_res = self.client.get(f'/api/courses/{self.course.id}/curriculum/')
        self.assertEqual(curriculum_res.status_code, status.HTTP_200_OK)
        self.assertEqual(curriculum_res.data['course_title'], 'JEE Advanced Test Course')
        self.assertEqual(len(curriculum_res.data['subjects']), 1)
        self.assertEqual(curriculum_res.data['subjects'][0]['chapters'][0]['lessons'][0]['title'], 'Lesson 1: Projectile Motion')

    def test_04_lms_video_progress(self):
        """Test student marking video completion"""
        self.client.force_authenticate(user=self.student)
        res = self.client.post(f'/api/videos/{self.lesson.id}/progress/', {
            'is_completed': True,
            'watched_duration_seconds': 2700
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_completed'])
        self.assertEqual(res.data['watched_duration_seconds'], 2700)

    def test_05_online_test_and_evaluation(self):
        """Test starting test and submitting answers for instant scoring"""
        test_obj = Test.objects.create(
            title='Physics Quiz 1',
            course=self.course,
            duration_minutes=30,
            total_marks=8,
            passing_marks=4
        )
        q1 = Question.objects.create(
            test=test_obj,
            question_text='What is the acceleration due to gravity on Earth?',
            option_a='9.8 m/s²',
            option_b='5.0 m/s²',
            option_c='15.0 m/s²',
            option_d='Zero',
            correct_option='A',
            marks=4.0,
            negative_marks=1.0,
            order=1
        )
        q2 = Question.objects.create(
            test=test_obj,
            question_text='Unit of force is:',
            option_a='Joule',
            option_b='Newton',
            option_c='Watt',
            option_d='Pascal',
            correct_option='B',
            marks=4.0,
            negative_marks=1.0,
            order=2
        )

        self.client.force_authenticate(user=self.student)
        start_res = self.client.post(f'/api/tests/{test_obj.id}/start/', {})
        self.assertEqual(start_res.status_code, status.HTTP_200_OK)
        attempt_id = start_res.data['attempt_id']

        # Submit answers: Q1 correct (A), Q2 correct (B)
        submit_res = self.client.post(f'/api/tests/{test_obj.id}/submit/', {
            'attempt_id': attempt_id,
            'answers': [
                {'question_id': q1.id, 'selected_option': 'A'},
                {'question_id': q2.id, 'selected_option': 'B'},
            ]
        }, format='json')
        self.assertEqual(submit_res.status_code, status.HTTP_200_OK)
        self.assertEqual(float(submit_res.data['score']), 8.0)
        self.assertEqual(float(submit_res.data['percentage']), 100.0)
        self.assertTrue(submit_res.data['is_passed'])

    def test_06_attendance_and_fee_simulation(self):
        """Test attendance marking and fee online payment simulation"""
        batch = Batch.objects.create(
            name='Test Alpha Batch',
            code='BATCH-TST-A1',
            course=self.course,
            start_date='2026-08-01'
        )

        # Teacher marks attendance
        self.client.force_authenticate(user=self.teacher)
        att_res = self.client.post('/api/attendance/', {
            'batch_id': batch.id,
            'date': '2026-08-26',
            'records': [
                {'student_id': self.student.id, 'status': 'PRESENT', 'remarks': 'Great participation'}
            ]
        }, format='json')
        self.assertEqual(att_res.status_code, status.HTTP_200_OK)

        # Fee payment simulation
        fee = FeeRecord.objects.create(
            student=self.student,
            course=self.course,
            invoice_number='INV-TEST-001',
            total_amount=15000.00,
            paid_amount=0.00,
            due_date='2026-09-01',
            status='PENDING'
        )

        self.client.force_authenticate(user=self.student)
        pay_res = self.client.post(f'/api/fees/{fee.id}/pay/', {
            'payment_mode': 'UPI',
            'amount': 15000.00
        })
        self.assertEqual(pay_res.status_code, status.HTTP_200_OK)
        self.assertEqual(pay_res.data['invoice']['status'], 'PAID')

    def test_07_public_inquiry(self):
        """Test public contact inquiry submission"""
        res = self.client.post('/api/inquiries/', {
            'full_name': 'Test Lead User',
            'email': 'lead@example.com',
            'phone': '+91 99999 88888',
            'course_interested': 'JEE Advanced',
            'current_class': 'Class 11',
            'message': 'Please share brochure'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
