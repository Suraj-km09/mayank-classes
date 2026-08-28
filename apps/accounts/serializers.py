from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, StudentProfile, TeacherProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'roll_number', 'target_exam', 'current_class',
            'school_or_college', 'parent_name', 'parent_phone',
            'date_of_birth', 'admission_date', 'emergency_contact'
        ]

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'employee_id', 'designation', 'qualification',
            'experience_years', 'specialization', 'bio', 'rating',
            'total_students_mentored'
        ]

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    teacher_profile = TeacherProfileSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'phone', 'avatar_url', 'city', 'address',
            'student_profile', 'teacher_profile', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # Allow login via username or email
        user = User.objects.filter(username=username_or_email).first()
        if not user:
            user = User.objects.filter(email=username_or_email).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("This account has been deactivated.")
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials. Please check your username/email and password.")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    target_exam = serializers.CharField(required=False, default='JEE / NEET')
    current_class = serializers.CharField(required=False, default='Class 11')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone', 'target_exam', 'current_class']

    def create(self, validated_data):
        target_exam = validated_data.pop('target_exam', 'JEE / NEET')
        current_class = validated_data.pop('current_class', 'Class 11')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            role=User.Role.STUDENT,
            **validated_data
        )
        user.set_password(password)
        user.save()

        # Create StudentProfile
        import random
        roll_num = f"MC-{random.randint(10000, 99999)}"
        StudentProfile.objects.create(
            user=user,
            roll_number=roll_num,
            target_exam=target_exam,
            current_class=current_class
        )
        return user
