from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academic.models import Course, Batch

class Test(TimeStampedModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='tests')
    duration_minutes = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=40)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    instructions = models.TextField(default='1. Each MCQ contains 4 marks.\n2. Negative marking: -1 for incorrect answers.\n3. Do not refresh during the examination.')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Question(TimeStampedModel):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(max_length=2, choices=OPTION_CHOICES)
    marks = models.DecimalField(max_digits=4, decimal_places=1, default=4.0)
    negative_marks = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    explanation = models.TextField(blank=True, null=True, help_text='Detailed step-by-step solution')
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}..."


class StudentTestAttempt(TimeStampedModel):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('SUBMITTED', 'Submitted & Evaluated'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    submit_time = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    total_possible_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100.0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_passed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')

    class Meta:
        ordering = ['-submit_time', '-start_time']

    def __str__(self):
        return f"{self.student.username} - {self.test.title}: {self.score}/{self.total_possible_marks}"


class StudentAnswer(TimeStampedModel):
    attempt = models.ForeignKey(StudentTestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    selected_option = models.CharField(max_length=2, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.student.username} Q{self.question.order}: {self.selected_option} ({'Correct' if self.is_correct else 'Wrong'})"
