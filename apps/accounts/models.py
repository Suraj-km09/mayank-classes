from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        TEACHER = 'TEACHER', 'Teacher / Faculty'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text='Designates the role of the user in the coaching institute.'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True, help_text='Profile image URL or avatar')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_teacher_role(self):
        return self.role == self.Role.TEACHER

    def is_student_role(self):
        return self.role == self.Role.STUDENT

    def get_full_name_display(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    def __str__(self):
        return f"{self.get_full_name_display()} ({self.role})"


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True)
    target_exam = models.CharField(max_length=100, default='JEE Main / Advanced')
    current_class = models.CharField(max_length=50, default='Class 11')
    school_or_college = models.CharField(max_length=255, blank=True, null=True)
    parent_name = models.CharField(max_length=150, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Student: {self.roll_number} - {self.user.get_full_name_display()}"


class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=150, default='Senior Faculty')
    qualification = models.CharField(max_length=255, default='B.Tech / M.Sc')
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=5.0)
    specialization = models.CharField(max_length=255, default='Physics')
    bio = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9)
    total_students_mentored = models.IntegerField(default=1500)

    def __str__(self):
        return f"Faculty: {self.user.get_full_name_display()} ({self.specialization})"
