from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Course(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('FOUNDATION', 'Foundation Programs (Classes 6-10)'),
        ('ENGINEERING', 'JEE Preparation (Main & Advanced)'),
        ('MEDICAL', 'NEET Preparation (Medical Entrance)'),
        ('OTHER_EXAMS', 'Other Competitive Exams (CUET, NDA, Olympiads)'),
        ('BOARDS', 'Target Board Excellence (Class 11-12)'),
        ('CRASH_COURSE', 'Fast-Track Crash Course & Test Series'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ENGINEERING')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    target_class = models.CharField(max_length=50, default='Class 11 & 12')
    duration_weeks = models.IntegerField(default=52)
    mode = models.CharField(max_length=100, default='Offline Classroom & Live Hybrid')
    badge_text = models.CharField(max_length=100, blank=True, null=True, help_text='e.g. MOST POPULAR, IIT FOCUSED, FOUNDATION')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=45000.00)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    features = models.JSONField(default=list, blank=True, help_text='List of key bullet highlights')
    overview_data = models.JSONField(default=dict, blank=True, help_text='Structured overview, pedagogy, and target eligibility')
    faqs = models.JSONField(default=list, blank=True, help_text='List of {question, answer} dicts')
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-is_featured', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class Subject(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    icon = models.CharField(max_length=100, default='book-open')
    color_accent = models.CharField(max_length=50, default='#3B82F6')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.course.title} → {self.name}"


class Chapter(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    chapter_number = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, default=8.0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'chapter_number']

    def __str__(self):
        return f"Ch {self.chapter_number}: {self.title} ({self.subject.name})"


class Batch(TimeStampedModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    schedule_time = models.CharField(max_length=150, default='Mon, Wed, Fri (4:00 PM - 7:30 PM)')
    classroom = models.CharField(max_length=100, default='Lecture Hall Alpha-1')
    mode = models.CharField(max_length=50, choices=[('OFFLINE', 'Offline Classroom'), ('ONLINE', 'Live Interactive'), ('HYBRID', 'Hybrid')], default='HYBRID')
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_batches', blank=True)
    max_capacity = models.IntegerField(default=40)

    def __str__(self):
        return f"{self.name} [{self.code}] - {self.course.title}"


class BatchEnrollment(TimeStampedModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        unique_together = ('batch', 'student')

    def __str__(self):
        return f"{self.student.get_full_name_display()} in {self.batch.name}"
