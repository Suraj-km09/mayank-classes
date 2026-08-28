from django.contrib import admin
from .models import Attendance, FeeRecord, Certificate

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'batch', 'status', 'marked_by')
    list_filter = ('status', 'batch', 'date')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'course', 'total_amount', 'paid_amount', 'status', 'due_date')
    list_filter = ('status', 'payment_mode')
    search_fields = ('invoice_number', 'student__first_name', 'student__last_name')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'student', 'course', 'grade', 'issue_date')
    search_fields = ('certificate_number', 'student__first_name', 'student__last_name')
