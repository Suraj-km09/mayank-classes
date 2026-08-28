from django.urls import path
from .views import (
    TestListView, TestDetailView,
    StartTestView, SubmitTestView,
    TestAttemptDetailView, StudentAttemptsListView
)

urlpatterns = [
    path('tests/', TestListView.as_view(), name='api-tests'),
    path('tests/<int:id>/', TestDetailView.as_view(), name='api-test-detail'),
    path('tests/<int:test_id>/start/', StartTestView.as_view(), name='api-test-start'),
    path('tests/<int:test_id>/submit/', SubmitTestView.as_view(), name='api-test-submit'),
    path('attempts/', StudentAttemptsListView.as_view(), name='api-attempts-list'),
    path('attempts/<int:id>/', TestAttemptDetailView.as_view(), name='api-attempt-detail'),
]
