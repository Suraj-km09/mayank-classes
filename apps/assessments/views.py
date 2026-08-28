from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Test, Question, StudentTestAttempt, StudentAnswer
from .serializers import (
    TestListSerializer, QuestionSerializer,
    QuestionStudentViewSerializer, StudentTestAttemptSerializer
)
from apps.core.permissions import IsTeacherOrAdmin

class TestListView(generics.ListCreateAPIView):
    serializer_class = TestListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Test.objects.filter(is_published=True)
        course_id = self.request.query_params.get('course_id')
        batch_id = self.request.query_params.get('batch_id')

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
            
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestListSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

class StartTestView(APIView):
    """
    Student initiates a test. Creates or resumes an attempt and returns test questions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id, is_published=True)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found or unpublished.'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create attempt
        attempt, created = StudentTestAttempt.objects.get_or_create(
            student=request.user,
            test=test,
            status='IN_PROGRESS',
            defaults={
                'total_possible_marks': test.total_marks
            }
        )

        questions = test.questions.all().order_by('order')
        questions_data = QuestionStudentViewSerializer(questions, many=True).data

        return Response({
            'attempt_id': attempt.id,
            'test_id': test.id,
            'test_title': test.title,
            'duration_minutes': test.duration_minutes,
            'total_marks': test.total_marks,
            'passing_marks': test.passing_marks,
            'instructions': test.instructions,
            'questions': questions_data
        })

class SubmitTestView(APIView):
    """
    Evaluates submitted answers, calculates score & percentage, stores answer breakdown.
    Expected payload:
    {
        "attempt_id": 1,
        "answers": [
            {"question_id": 10, "selected_option": "A"},
            {"question_id": 11, "selected_option": "C"}
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found.'}, status=status.HTTP_404_NOT_FOUND)

        attempt_id = request.data.get('attempt_id')
        answers_data = request.data.get('answers', [])
        if isinstance(answers_data, str):
            import json
            try:
                answers_data = json.loads(answers_data)
            except Exception:
                answers_data = []

        if attempt_id:
            attempt = StudentTestAttempt.objects.filter(id=attempt_id, student=request.user).first()
        else:
            attempt = StudentTestAttempt.objects.filter(test=test, student=request.user, status='IN_PROGRESS').first()

        if not attempt:
            attempt = StudentTestAttempt.objects.create(
                student=request.user,
                test=test,
                total_possible_marks=test.total_marks
            )

        total_score = 0.0
        questions_map = {q.id: q for q in test.questions.all()}

        # Clear existing answers if any re-attempt
        attempt.answers.all().delete()

        for ans in answers_data:
            q_id = ans.get('question_id')
            selected = (ans.get('selected_option') or '').strip().upper()
            
            if q_id in questions_map:
                question = questions_map[q_id]
                is_correct = (selected == question.correct_option)
                
                if is_correct:
                    marks_awarded = float(question.marks)
                elif selected:
                    marks_awarded = -float(question.negative_marks)
                else:
                    marks_awarded = 0.0

                total_score += marks_awarded

                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected if selected else None,
                    is_correct=is_correct,
                    marks_awarded=marks_awarded
                )

        total_score = max(0.0, total_score)
        total_possible = float(test.total_marks) if test.total_marks > 0 else 100.0
        percentage = (total_score / total_possible) * 100.0 if total_possible else 0.0
        is_passed = total_score >= float(test.passing_marks)

        attempt.score = total_score
        attempt.percentage = round(percentage, 2)
        attempt.is_passed = is_passed
        attempt.status = 'SUBMITTED'
        attempt.submit_time = timezone.now()
        attempt.save()

        serializer = StudentTestAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAttemptDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentTestAttemptSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher_role() or user.is_admin_role():
            return StudentTestAttempt.objects.all()
        return StudentTestAttempt.objects.filter(student=user)

class StudentAttemptsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentTestAttemptSerializer

    def get_queryset(self):
        user = self.request.user
        test_id = self.request.query_params.get('test_id')
        queryset = StudentTestAttempt.objects.filter(status='SUBMITTED')

        if not (user.is_teacher_role() or user.is_admin_role()):
            queryset = queryset.filter(student=user)
            
        if test_id:
            queryset = queryset.filter(test_id=test_id)
        return queryset
