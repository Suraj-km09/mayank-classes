from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from apps.core.views import (
    home_view, login_view, student_portal_view,
    teacher_portal_view, admin_portal_view, certificate_verify_view,
    courses_catalog_view, category_hub_view, course_detail_view,
    recorded_courses_view, study_materials_view,
    faculty_view, results_view, about_view, contact_view, photos_view
)

urlpatterns = [
    # Django Default Admin Panel
    path('admin/', admin.site.urls),
    path('django-admin/', RedirectView.as_view(url='/admin/', permanent=False)),

    # Public Course Ecosystem & Marketing Web Views
    path('', home_view, name='home'),
    path('courses/', courses_catalog_view, name='courses-catalog'),
    path('courses/foundation/', category_hub_view, {'category_slug': 'foundation'}, name='category-foundation'),
    path('courses/jee/', category_hub_view, {'category_slug': 'jee'}, name='category-jee'),
    path('courses/neet/', category_hub_view, {'category_slug': 'neet'}, name='category-neet'),
    path('courses/other-exams/', category_hub_view, {'category_slug': 'other-exams'}, name='category-other-exams'),
    path('courses/<slug:slug>/', course_detail_view, name='course-detail'),
    
    # Study & Recorded Courses Hubs
    path('recorded-courses/', recorded_courses_view, name='recorded-courses'),
    path('online-courses/', recorded_courses_view, name='online-courses'),
    path('study-materials/', study_materials_view, name='study-materials'),
    
    # Institution Info & Portals
    path('faculty/', faculty_view, name='faculty'),
    path('results/', results_view, name='results'),
    path('about/', about_view, name='about'),
    path('photos/', photos_view, name='photos'),
    path('contact/', contact_view, name='contact'),

    # Portals & Auth
    path('login/', login_view, name='login'),
    path('student/', student_portal_view, name='student-portal'),
    path('teacher/', teacher_portal_view, name='teacher-portal'),
    path('admin-portal/', admin_portal_view, name='admin-portal'),
    path('verify-certificate/<str:code>/', certificate_verify_view, name='certificate-verify-page'),
    path('verify-certificate/', certificate_verify_view, name='certificate-verify-search'),

    # REST APIs
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.academic.urls')),
    path('api/', include('apps.lms.urls')),
    path('api/', include('apps.assessments.urls')),
    path('api/', include('apps.operations.urls')),
    path('api/', include('apps.portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
