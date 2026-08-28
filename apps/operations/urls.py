from django.urls import path
from .views import (
    AttendanceListView, StudentAttendanceStatsView,
    FeeRecordListView, FeePaySimulationView,
    CertificateListView, CertificateVerifyView
)

urlpatterns = [
    path('attendance/', AttendanceListView.as_view(), name='api-attendance'),
    path('attendance/stats/', StudentAttendanceStatsView.as_view(), name='api-attendance-stats'),
    path('fees/', FeeRecordListView.as_view(), name='api-fees'),
    path('fees/<int:invoice_id>/pay/', FeePaySimulationView.as_view(), name='api-fee-pay'),
    path('certificates/', CertificateListView.as_view(), name='api-certificates'),
    path('certificates/verify/<str:code>/', CertificateVerifyView.as_view(), name='api-certificate-verify'),
]
