import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academic.models import Batch, Course

class Attendance(TimeStampedModel):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('EXCUSED', 'Excused'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendances')
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('batch', 'student', 'date')
        ordering = ['-date', 'student__first_name']

    def __str__(self):
        return f"{self.date} | {self.student.get_full_name_display()} - {self.get_status_display()}"


class FeeRecord(TimeStampedModel):
    STATUS_CHOICES = [
        ('PAID', 'Fully Paid'),
        ('PARTIAL', 'Partially Paid'),
        ('PENDING', 'Payment Pending'),
        ('OVERDUE', 'Payment Overdue'),
    ]

    PAYMENT_MODES = [
        ('UPI', 'UPI / QR Code'),
        ('NETBANKING', 'Net Banking / NEFT'),
        ('CARD', 'Credit / Debit Card'),
        ('CASH', 'Cash Counter Receipt'),
        ('CHEQUE', 'Cheque / DD'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fee_records')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='fee_records')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    
    invoice_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200, default='Course Tuition & Exam Preparation Fee')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    payment_mode = models.CharField(max_length=30, choices=PAYMENT_MODES, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_url = models.URLField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-due_date', '-id']

    @property
    def due_amount(self):
        return max(0.0, float(self.total_amount) - float(self.paid_amount))

    def __str__(self):
        return f"Inv #{self.invoice_number} - {self.student.get_full_name_display()} ({self.status})"


class Certificate(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, default='Certificate of Academic Excellence')
    issue_date = models.DateField()
    grade = models.CharField(max_length=20, default='A+ (Distinction)')
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(default='Has successfully completed the advanced classroom coaching curriculum with outstanding marks.')
    certificate_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.certificate_number} - {self.student.get_full_name_display()} ({self.course.title})"
