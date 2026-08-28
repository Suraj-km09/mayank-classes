from django.contrib import admin
from .models import Test, Question, StudentTestAttempt, StudentAnswer

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'batch', 'duration_minutes', 'total_marks', 'is_published')
    list_filter = ('course', 'is_published')
    search_fields = ('title', 'instructions')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'test', 'question_text', 'correct_option', 'marks')
    list_filter = ('test',)

@admin.register(StudentTestAttempt)
class StudentTestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'total_possible_marks', 'percentage', 'is_passed', 'status', 'submit_time')
    list_filter = ('is_passed', 'status', 'test')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'marks_awarded')
