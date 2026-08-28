from django.db import models
from apps.core.models import TimeStampedModel

class Notice(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('URGENT', 'Urgent Announcement'),
        ('EXAM', 'Exam & Test Schedule'),
        ('HOLIDAY', 'Holiday Notice'),
        ('EVENT', 'Workshop & Special Seminar'),
        ('GENERAL', 'General Update'),
    ]

    TARGET_ROLE_CHOICES = [
        ('ALL', 'All Users & Public'),
        ('STUDENT', 'Students Only'),
        ('TEACHER', 'Faculty Only'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='GENERAL')
    target_role = models.CharField(max_length=50, choices=TARGET_ROLE_CHOICES, default='ALL')
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)
    attachment_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-is_pinned', '-published_date', '-id']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class Testimonial(TimeStampedModel):
    student_name = models.CharField(max_length=150)
    course_name = models.CharField(max_length=150, default='JEE Advanced 2-Year Classroom')
    score_or_rank = models.CharField(max_length=100, default='AIR 142 (JEE Advanced)')
    college_admitted = models.CharField(max_length=200, default='IIT Bombay (Computer Science)')
    review_text = models.TextField()
    rating = models.IntegerField(default=5)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    year = models.IntegerField(default=2025)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', '-rating']

    def __str__(self):
        return f"{self.student_name} - {self.score_or_rank}"


class SuccessStory(TimeStampedModel):
    student_name = models.CharField(max_length=150)
    exam_name = models.CharField(max_length=150, default='JEE Advanced')
    rank_or_score = models.CharField(max_length=100, default='AIR 48')
    image_url = models.URLField(max_length=500, blank=True, null=True)
    summary = models.CharField(max_length=300)
    story = models.TextField()
    year = models.IntegerField(default=2025)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', 'id']

    def __str__(self):
        return f"Topper: {self.student_name} ({self.rank_or_score})"


class GalleryImage(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('CAMPUS', 'Modern Campus & Classrooms'),
        ('LABS', 'Advanced Science & Computer Labs'),
        ('AWARDS', 'Felicitation & Award Ceremonies'),
        ('EVENTS', 'Seminars & Doubt Clearing Workshops'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='CAMPUS')
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class ContactInquiry(TimeStampedModel):
    STATUS_CHOICES = [
        ('NEW', 'New Inquiry'),
        ('CONTACTED', 'Counselor Contacted'),
        ('CONVERTED', 'Enrolled'),
        ('CLOSED', 'Closed'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course_interested = models.CharField(max_length=200, default='JEE Main & Advanced')
    current_class = models.CharField(max_length=50, default='Class 11')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry: {self.full_name} ({self.course_interested}) - {self.status}"
