from rest_framework import serializers
from .models import Test, Question, StudentTestAttempt, StudentAnswer
from apps.accounts.serializers import UserSerializer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'test', 'question_text', 'option_a', 'option_b',
            'option_c', 'option_d', 'correct_option', 'marks',
            'negative_marks', 'explanation', 'order'
        ]

class QuestionStudentViewSerializer(serializers.ModelSerializer):
    """Hides correct_option and explanation during active test taking."""
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'option_a', 'option_b',
            'option_c', 'option_d', 'marks', 'negative_marks', 'order'
        ]

class TestListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True, default='All Batches')
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    user_attempt_status = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            'id', 'title', 'course', 'course_title', 'batch', 'batch_name',
            'duration_minutes', 'total_marks', 'passing_marks',
            'start_time', 'end_time', 'instructions', 'questions_count',
            'is_published', 'user_attempt_status'
        ]

    def get_user_attempt_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            attempt = StudentTestAttempt.objects.filter(student=request.user, test=obj).order_by('-id').first()
            if attempt:
                return {
                    'attempt_id': attempt.id,
                    'status': attempt.status,
                    'score': float(attempt.score),
                    'total_possible_marks': float(attempt.total_possible_marks),
                    'percentage': float(attempt.percentage),
                    'is_passed': attempt.is_passed,
                    'submit_time': attempt.submit_time
                }
        return None

class StudentAnswerSerializer(serializers.ModelSerializer):
    question_details = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = ['id', 'question', 'selected_option', 'is_correct', 'marks_awarded', 'question_details']

class StudentTestAttemptSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    test_title = serializers.CharField(source='test.title', read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = StudentTestAttempt
        fields = [
            'id', 'student', 'student_details', 'test', 'test_title',
            'start_time', 'submit_time', 'score', 'total_possible_marks',
            'percentage', 'is_passed', 'status', 'answers'
        ]
