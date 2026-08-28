from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VideoLesson, VideoProgress, StudyMaterial
from .serializers import VideoLessonSerializer, VideoProgressSerializer, StudyMaterialSerializer
from apps.academic.models import Course, Subject, Chapter
from apps.core.permissions import IsTeacherOrAdmin

class VideoLessonListView(generics.ListCreateAPIView):
    serializer_class = VideoLessonSerializer

    def get_queryset(self):
        queryset = VideoLesson.objects.filter(is_published=True)
        course_id = self.request.query_params.get('course_id')
        subject_id = self.request.query_params.get('subject_id')
        chapter_id = self.request.query_params.get('chapter_id')
        is_free_preview = self.request.query_params.get('is_free_preview')

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        if is_free_preview:
            queryset = queryset.filter(is_free_preview=True)

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class VideoLessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

class VideoProgressUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, video_id):
        try:
            video = VideoLesson.objects.get(id=video_id)
        except VideoLesson.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_completed = request.data.get('is_completed', False)
        last_pos = request.data.get('last_position_seconds', 0)
        watched_dur = request.data.get('watched_duration_seconds', 0)

        progress, created = VideoProgress.objects.get_or_create(
            student=request.user,
            video=video
        )
        if is_completed is not None:
            progress.is_completed = bool(is_completed)
        if last_pos:
            progress.last_position_seconds = int(last_pos)
        if watched_dur:
            progress.watched_duration_seconds = max(progress.watched_duration_seconds, int(watched_dur))
        
        progress.save()
        return Response(VideoProgressSerializer(progress).data, status=status.HTTP_200_OK)

class StudyMaterialListView(generics.ListCreateAPIView):
    serializer_class = StudyMaterialSerializer

    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(is_published=True)
        course_id = self.request.query_params.get('course_id')
        subject_id = self.request.query_params.get('subject_id')
        material_type = self.request.query_params.get('material_type')

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if material_type:
            queryset = queryset.filter(material_type=material_type)

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacherOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class CourseCurriculumView(APIView):
    """
    Returns full structured hierarchy for the LMS player:
    Course -> Subjects -> Chapters -> [Lessons, Materials]
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        subjects_data = []
        subjects = course.subjects.filter(is_active=True).prefetch_related('chapters__lessons')

        for subject in subjects:
            chapters_data = []
            for chapter in subject.chapters.filter(is_active=True):
                lessons = chapter.lessons.filter(is_published=True)
                materials = chapter.materials.filter(is_published=True)
                
                lessons_serializer = VideoLessonSerializer(lessons, many=True, context={'request': request})
                materials_serializer = StudyMaterialSerializer(materials, many=True, context={'request': request})

                chapters_data.append({
                    'id': chapter.id,
                    'title': chapter.title,
                    'chapter_number': chapter.chapter_number,
                    'estimated_hours': float(chapter.estimated_hours),
                    'lessons': lessons_serializer.data,
                    'materials': materials_serializer.data,
                })

            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'icon': subject.icon,
                'color_accent': subject.color_accent,
                'chapters': chapters_data,
            })

        return Response({
            'course_id': course.id,
            'course_title': course.title,
            'slug': course.slug,
            'category': course.category,
            'target_class': course.target_class,
            'subjects': subjects_data
        })
