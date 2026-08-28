from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Profile Info', {'fields': ('role', 'phone', 'avatar_url', 'city', 'address')}),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'target_exam', 'current_class', 'parent_phone')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'designation', 'specialization', 'experience_years', 'rating')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'specialization')
