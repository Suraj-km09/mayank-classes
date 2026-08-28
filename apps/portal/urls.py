from django.urls import path
from .views import (
    NoticeListView, NoticeDetailView, TestimonialListView,
    SuccessStoryListView, GalleryImageListView,
    ContactInquiryView, ContactInquiryDetailView,
    AdminDashboardStatsView,
    TeacherDashboardStatsView, StudentDashboardStatsView,
    ChatbotAssistantView
)

urlpatterns = [
    path('notices/', NoticeListView.as_view(), name='api-notices'),
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='api-notice-detail'),
    path('testimonials/', TestimonialListView.as_view(), name='api-testimonials'),
    path('toppers/', SuccessStoryListView.as_view(), name='api-toppers'),
    path('gallery/', GalleryImageListView.as_view(), name='api-gallery'),
    path('inquiries/', ContactInquiryView.as_view(), name='api-inquiries'),
    path('inquiries/<int:pk>/', ContactInquiryDetailView.as_view(), name='api-inquiry-detail'),
    path('admin/stats/', AdminDashboardStatsView.as_view(), name='api-admin-stats'),
    path('teacher/stats/', TeacherDashboardStatsView.as_view(), name='api-teacher-stats'),
    path('student/stats/', StudentDashboardStatsView.as_view(), name='api-student-stats'),
    path('chatbot/', ChatbotAssistantView.as_view(), name='api-chatbot'),
]

