from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from apps.academic.models import Course, Subject, Chapter, Batch
from apps.lms.models import VideoLesson, StudyMaterial
from apps.accounts.models import User
from apps.portal.models import SuccessStory, Testimonial, Notice, GalleryImage

# Slug alias map for convenient short URLs
SLUG_ALIASES = {
    'jee-main': 'jee-main-target',
    'jee-advanced': 'jee-advanced-pinnacle',
    'jee-dropper': 'jee-dropper-rankers',
    'neet-dropper': 'neet-dropper-achievers',
    'neet-complete': 'neet-medical-champions',
    'foundation-10': 'foundation-class-10',
    'foundation-9': 'foundation-class-9',
    'foundation-8': 'foundation-class-8',
    'foundation-7': 'foundation-class-7',
    'foundation-6': 'foundation-class-6',
    'cuet': 'cuet-ug-master',
    'nda': 'nda-defence-mastery',
}

CATEGORY_CONFIG = {
    'foundation': {
        'code': 'FOUNDATION',
        'title': 'Foundation Programs (Classes 6–10)',
        'subtitle': 'Building unshakeable cognitive intuition, analytical problem solving, and early Olympiad mastery.',
        'badge': 'FOUNDATION & OLYMPIAD',
        'accent_color': '#059669',
        'accent_bg': 'linear-gradient(135deg, #059669, #10B981)',
        'target_classes': ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10'],
        'icon': 'graduation-cap',
        'highlights': [
            'Early exposure to competitive STEM methodologies (IJSO, PRMO, NSO, IMO)',
            'School Board excellence guarantee with 95%+ marks track record',
            'Mental Ability, Logic & IQ grooming workshops',
            'Interactive animations, 3D science kits, and practical reasoning'
        ]
    },
    'jee': {
        'code': 'ENGINEERING',
        'title': 'IIT-JEE Preparation (Main & Advanced)',
        'subtitle': 'Comprehensive pedagogy for cracking NTA JEE Main and IIT-JEE Advanced with top All India Ranks.',
        'badge': 'IIT-JEE PINNACLE',
        'accent_color': '#7C3AED',
        'accent_bg': 'linear-gradient(135deg, #4338CA, #6366F1)',
        'target_classes': ['Class 11', 'Class 12', 'Dropper / Repeater'],
        'icon': 'atom',
        'highlights': [
            'Kota & Delhi master faculty with 15+ years of ranker-producing experience',
            'Computer-Based Testing (AI-CBT) lab simulating actual NTA interface',
            'Multi-tier problem sets: Level 1 (Main) → Level 2 (Adv) → Level 3 (Olympiad)',
            '12-Hour daily 1-on-1 doubt counters and personalized rank mentorship'
        ]
    },
    'neet': {
        'code': 'MEDICAL',
        'title': 'NEET-UG Medical Entrance Preparation',
        'subtitle': 'Rigorous medical entrance training crafted for AIIMS New Delhi and premier government medical colleges.',
        'badge': 'NEET MEDICAL CHAMPIONS',
        'accent_color': '#DC2626',
        'accent_bg': 'linear-gradient(135deg, #B91C1C, #E11D48)',
        'target_classes': ['Class 11', 'Class 12', 'Dropper / Repeater'],
        'icon': 'stethoscope',
        'highlights': [
            'Line-by-Line NCERT decoding in Botany & Zoology with 3D diagram modules',
            'Physics made simple for medical aspirants with speed-oriented shortcuts',
            '75+ Full-Length OMR Mock Tests with negative mark analysis',
            'Mentorship by top AIIMS alumni and experienced medical faculty'
        ]
    },
    'other-exams': {
        'code': 'OTHER_EXAMS',
        'title': 'Other Competitive & Entrance Exams',
        'subtitle': 'Specialized career programs for CUET (UG), UPSC NDA/NA, and National Talent Examinations.',
        'badge': 'COMPETITIVE CAREERS',
        'accent_color': '#0284C7',
        'accent_bg': 'linear-gradient(135deg, #0369A1, #0EA5E9)',
        'target_classes': ['Class 11', 'Class 12', '12th Passed'],
        'icon': 'award',
        'highlights': [
            'CUET (UG) General Test + Domain Subjects mapped to Central Universities',
            'UPSC NDA Written Mathematics + GAT + SSB Interview orientation',
            'High-speed calculation tricks and timed CBT mock exams',
            'Comprehensive guidance on central university admissions & cutoffs'
        ]
    }
}

def home_view(request):
    courses = Course.objects.filter(is_active=True).prefetch_related('subjects')
    featured_courses = courses.filter(is_featured=True)[:6]
    foundation_courses = courses.filter(category='FOUNDATION')[:4]
    jee_courses = courses.filter(category='ENGINEERING')[:4]
    neet_courses = courses.filter(category='MEDICAL')[:4]
    other_courses = courses.filter(category='OTHER_EXAMS')[:4]
    
    toppers = SuccessStory.objects.filter(is_featured=True)[:6]
    teachers = User.objects.filter(role='TEACHER').prefetch_related('teacher_profile')[:4]
    notices = Notice.objects.filter(target_role__in=['ALL', 'STUDENT'])[:4]
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    gallery = GalleryImage.objects.all()[:6]

    context = {
        'featured_courses': featured_courses,
        'foundation_courses': foundation_courses,
        'jee_courses': jee_courses,
        'neet_courses': neet_courses,
        'other_courses': other_courses,
        'toppers': toppers,
        'teachers': teachers,
        'notices': notices,
        'testimonials': testimonials,
        'gallery': gallery,
    }
    return render(request, 'public/index.html', context)


def courses_catalog_view(request):
    courses = Course.objects.filter(is_active=True).prefetch_related('subjects__chapters', 'batches')
    
    # Category filter
    category = request.GET.get('category', 'ALL')
    class_filter = request.GET.get('class', 'ALL')
    search_query = request.GET.get('q', '')

    filtered_courses = courses
    if category and category != 'ALL':
        cat_code = category.upper()
        if cat_code in ['ENGINEERING', 'MEDICAL', 'FOUNDATION', 'OTHER_EXAMS']:
            filtered_courses = filtered_courses.filter(category=cat_code)
    
    if class_filter and class_filter != 'ALL':
        filtered_courses = filtered_courses.filter(target_class__icontains=class_filter)

    if search_query:
        filtered_courses = filtered_courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(subjects__name__icontains=search_query)
        ).distinct()

    context = {
        'all_courses': courses,
        'courses': filtered_courses,
        'foundation_courses': courses.filter(category='FOUNDATION'),
        'jee_courses': courses.filter(category='ENGINEERING'),
        'neet_courses': courses.filter(category='MEDICAL'),
        'other_courses': courses.filter(category='OTHER_EXAMS'),
        'active_category': category,
        'active_class': class_filter,
        'search_query': search_query,
        'categories_meta': CATEGORY_CONFIG,
    }
    return render(request, 'public/courses_catalog.html', context)


def category_hub_view(request, category_slug):
    category_slug = category_slug.lower()
    
    # Check if this slug is an alias to a specific course
    if category_slug in SLUG_ALIASES:
        return redirect('course-detail', slug=SLUG_ALIASES[category_slug])

    if category_slug not in CATEGORY_CONFIG:
        # Check if it's a course slug directly
        course_exists = Course.objects.filter(slug=category_slug, is_active=True).exists()
        if course_exists:
            return redirect('course-detail', slug=category_slug)
        return redirect('courses-catalog')

    config = CATEGORY_CONFIG[category_slug]
    courses = Course.objects.filter(category=config['code'], is_active=True).prefetch_related('subjects__chapters', 'batches')
    toppers = SuccessStory.objects.filter(is_featured=True)[:4]
    faculty = User.objects.filter(role='TEACHER').prefetch_related('teacher_profile')[:4]

    context = {
        'category_key': category_slug,
        'config': config,
        'courses': courses,
        'toppers': toppers,
        'faculty': faculty,
    }
    return render(request, 'public/category_hub.html', context)


def course_detail_view(request, slug):
    # Resolve alias if present
    actual_slug = SLUG_ALIASES.get(slug, slug)
    course = get_object_or_404(
        Course.objects.prefetch_related(
            'subjects__chapters__lessons',
            'subjects__chapters__materials',
            'batches__teachers'
        ),
        slug=actual_slug,
        is_active=True
    )

    # Related courses in the same category
    related_courses = Course.objects.filter(
        category=course.category,
        is_active=True
    ).exclude(id=course.id)[:3]

    # Category meta configuration
    cat_key = 'foundation'
    for k, v in CATEGORY_CONFIG.items():
        if v['code'] == course.category:
            cat_key = k
            break
    cat_meta = CATEGORY_CONFIG.get(cat_key, CATEGORY_CONFIG['jee'])

    toppers = SuccessStory.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    faculty = User.objects.filter(role='TEACHER').prefetch_related('teacher_profile')[:4]
    
    # Calculate stats
    total_chapters = sum(s.chapters.count() for s in course.subjects.all())
    total_lessons = sum(
        sum(ch.lessons.count() for ch in s.chapters.all()) 
        for s in course.subjects.all()
    )

    context = {
        'course': course,
        'related_courses': related_courses,
        'cat_key': cat_key,
        'cat_meta': cat_meta,
        'toppers': toppers,
        'testimonials': testimonials,
        'faculty': faculty,
        'total_chapters': total_chapters,
        'total_lessons': total_lessons,
    }
    return render(request, 'public/course_detail.html', context)


def recorded_courses_view(request):
    courses = Course.objects.filter(is_active=True).prefetch_related(
        'subjects__chapters__lessons',
        'video_lessons'
    )
    
    category = request.GET.get('category', 'ALL')
    if category != 'ALL':
        courses = courses.filter(category=category.upper())

    # Demo video lessons
    preview_lessons = VideoLesson.objects.filter(is_free_preview=True, is_published=True).select_related('course', 'subject', 'teacher')[:8]

    context = {
        'courses': courses,
        'preview_lessons': preview_lessons,
        'active_category': category,
    }
    return render(request, 'public/recorded_courses.html', context)


def study_materials_view(request):
    materials = StudyMaterial.objects.filter(is_published=True).select_related('course', 'subject', 'chapter', 'teacher')
    
    mat_type = request.GET.get('type', 'ALL')
    if mat_type != 'ALL':
        materials = materials.filter(material_type=mat_type)

    context = {
        'materials': materials,
        'active_type': mat_type,
        'courses': Course.objects.filter(is_active=True),
    }
    return render(request, 'public/study_materials.html', context)


def faculty_view(request):
    teachers = User.objects.filter(role='TEACHER').prefetch_related('teacher_profile')
    context = {
        'teachers': teachers
    }
    return render(request, 'public/faculty.html', context)


def results_view(request):
    toppers = SuccessStory.objects.all().order_by('-year', 'id')
    testimonials = Testimonial.objects.all().order_by('-year', '-rating')
    context = {
        'toppers': toppers,
        'testimonials': testimonials
    }
    return render(request, 'public/results.html', context)


def about_view(request):
    faculty_count = User.objects.filter(role='TEACHER').count()
    courses_count = Course.objects.filter(is_active=True).count()
    context = {
        'faculty_count': max(faculty_count, 25),
        'courses_count': max(courses_count, 12),
        'gallery': GalleryImage.objects.all()[:6]
    }
    return render(request, 'public/about.html', context)


def contact_view(request):
    courses = Course.objects.filter(is_active=True)
    context = {
        'courses': courses
    }
    return render(request, 'public/contact.html', context)


def login_view(request):
    return render(request, 'auth/login.html')

def student_portal_view(request):
    return render(request, 'student/index.html')

def teacher_portal_view(request):
    return render(request, 'teacher/index.html')

def admin_portal_view(request):
    return render(request, 'portal/admin/index.html')

def certificate_verify_view(request, code=''):
    return render(request, 'public/certificate_verify.html', {'code': code})
