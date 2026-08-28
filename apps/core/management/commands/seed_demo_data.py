import datetime
import random
import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User, StudentProfile, TeacherProfile
from apps.academic.models import Course, Subject, Chapter, Batch, BatchEnrollment
from apps.lms.models import VideoLesson, VideoProgress, StudyMaterial
from apps.assessments.models import Test, Question, StudentTestAttempt, StudentAnswer
from apps.operations.models import Attendance, FeeRecord, Certificate
from apps.portal.models import Notice, Testimonial, SuccessStory, GalleryImage, ContactInquiry

class Command(BaseCommand):
    help = 'Seeds database with realistic demo data for Mayank Classes Coaching Platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing records and seeding demo data...'))

        # Clean all existing records
        ContactInquiry.objects.all().delete()
        GalleryImage.objects.all().delete()
        SuccessStory.objects.all().delete()
        Testimonial.objects.all().delete()
        Notice.objects.all().delete()
        Certificate.objects.all().delete()
        FeeRecord.objects.all().delete()
        Attendance.objects.all().delete()
        StudentAnswer.objects.all().delete()
        StudentTestAttempt.objects.all().delete()
        Question.objects.all().delete()
        Test.objects.all().delete()
        StudyMaterial.objects.all().delete()
        VideoProgress.objects.all().delete()
        VideoLesson.objects.all().delete()
        BatchEnrollment.objects.all().delete()
        Batch.objects.all().delete()
        Chapter.objects.all().delete()
        Subject.objects.all().delete()
        Course.objects.all().delete()
        StudentProfile.objects.all().delete()
        TeacherProfile.objects.all().delete()
        User.objects.all().delete()

        # ==========================================
        # 1. CREATE USERS (Admin, Teachers, Students)
        # ==========================================
        # Super Admin
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@mayankclasses.com',
            password='admin123',
            first_name='Mayank',
            last_name='Agrawal',
            role=User.Role.ADMIN,
            phone='+91 98765 43210',
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80',
            city='Kota / Delhi'
        )

        # Faculty
        teacher_physics = User.objects.create_user(
            username='teacher',
            email='teacher@mayankclasses.com',
            password='teacher123',
            first_name='Dr. Rajesh',
            last_name='Sharma',
            role=User.Role.TEACHER,
            phone='+91 98111 22334',
            avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80',
            city='Delhi'
        )
        TeacherProfile.objects.create(
            user=teacher_physics,
            employee_id='FAC-PHY-01',
            designation='Head of Department (Physics)',
            qualification='Ph.D. & M.Tech (IIT Roorkee)',
            experience_years=14.5,
            specialization='Mechanics & Electrodynamics',
            bio='Mentored 45+ Top-100 AIR rankers in JEE Advanced with over 14 years of teaching excellence.',
            rating=4.95,
            total_students_mentored=3800
        )

        teacher_chem = User.objects.create_user(
            username='dr_anjali',
            email='teacher.chemistry@mayankclasses.com',
            password='teacher123',
            first_name='Dr. Anjali',
            last_name='Verma',
            role=User.Role.TEACHER,
            phone='+91 98222 33445',
            avatar_url='https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80',
            city='Kota'
        )
        TeacherProfile.objects.create(
            user=teacher_chem,
            employee_id='FAC-CHM-02',
            designation='Senior Chemistry Specialist',
            qualification='M.Sc. Organic Chemistry (Gold Medalist, DU)',
            experience_years=11.0,
            specialization='Organic & Physical Chemistry',
            bio='Renowned for simplifying organic reaction mechanisms and visual physical chemistry models.',
            rating=4.90,
            total_students_mentored=2900
        )

        teacher_maths = User.objects.create_user(
            username='prof_vikram',
            email='teacher.maths@mayankclasses.com',
            password='teacher123',
            first_name='Prof. Vikram',
            last_name='Mehta',
            role=User.Role.TEACHER,
            phone='+91 98333 44556',
            avatar_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80',
            city='Delhi'
        )
        TeacherProfile.objects.create(
            user=teacher_maths,
            employee_id='FAC-MTH-03',
            designation='Lead Mathematics Guru',
            qualification='B.Tech & M.Tech (IIT Delhi)',
            experience_years=12.0,
            specialization='Calculus, Algebra & Vector Geometry',
            bio='Author of 3 best-selling JEE problem books with unique short-cut techniques.',
            rating=4.92,
            total_students_mentored=3400
        )

        teacher_bio = User.objects.create_user(
            username='dr_sneha',
            email='teacher.biology@mayankclasses.com',
            password='teacher123',
            first_name='Dr. Sneha',
            last_name='Kulkarni',
            role=User.Role.TEACHER,
            phone='+91 98444 55667',
            avatar_url='https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&auto=format&fit=crop&q=80',
            city='Pune'
        )
        TeacherProfile.objects.create(
            user=teacher_bio,
            employee_id='FAC-BIO-04',
            designation='Dean of Medical Academics',
            qualification='MBBS, MD (AIIMS New Delhi)',
            experience_years=9.5,
            specialization='Human Physiology & Genetics',
            bio='Expert in NCERT deep-decoding and clinical mnemonics for high-yield NEET scores.',
            rating=4.98,
            total_students_mentored=2600
        )

        # Primary Demo Student
        demo_student = User.objects.create_user(
            username='student',
            email='student@mayankclasses.com',
            password='student123',
            first_name='Aarav',
            last_name='Sharma',
            role=User.Role.STUDENT,
            phone='+91 98760 11223',
            avatar_url='https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=300&auto=format&fit=crop&q=80',
            city='Jaipur'
        )
        StudentProfile.objects.create(
            user=demo_student,
            roll_number='MC-2026-001',
            target_exam='JEE Advanced 2026',
            current_class='Class 12',
            school_or_college='Delhi Public School (DPS)',
            parent_name='Suresh Sharma',
            parent_phone='+91 98760 99887',
            date_of_birth=datetime.date(2008, 4, 15),
            emergency_contact='+91 98760 99887'
        )

        # Additional Students
        students_info = [
            ('priya_patel', 'priya.patel@mayankclasses.com', 'Priya', 'Patel', 'MC-2026-002', 'NEET-UG 2026', 'Class 12', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&auto=format&fit=crop&q=80'),
            ('rohit_verma', 'rohit.verma@mayankclasses.com', 'Rohit', 'Verma', 'MC-2026-003', 'JEE Main 2026', 'Class 12', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80'),
            ('ananya_gupta', 'ananya.gupta@mayankclasses.com', 'Ananya', 'Gupta', 'MC-2026-004', 'Foundation Class 10', 'Class 10', 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=300&auto=format&fit=crop&q=80'),
            ('kavya_nair', 'kavya.nair@mayankclasses.com', 'Kavya', 'Nair', 'MC-2026-005', 'NEET-UG 2027', 'Class 11', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&auto=format&fit=crop&q=80'),
            ('dev_singh', 'dev.singh@mayankclasses.com', 'Dev', 'Singh', 'MC-2026-006', 'JEE Advanced 2027', 'Class 11', 'https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=300&auto=format&fit=crop&q=80'),
        ]
        created_students = [demo_student]
        for u_name, email, f_name, l_name, roll, target, curr_cls, av_url in students_info:
            stu = User.objects.create_user(
                username=u_name,
                email=email,
                password='student123',
                first_name=f_name,
                last_name=l_name,
                role=User.Role.STUDENT,
                phone=f'+91 98{random.randint(10000000, 99999999)}',
                avatar_url=av_url,
                city='Delhi / NCR'
            )
            StudentProfile.objects.create(
                user=stu,
                roll_number=roll,
                target_exam=target,
                current_class=curr_cls,
                school_or_college='DAV Public School',
                parent_name=f'Mr. {l_name}',
                parent_phone=f'+91 99{random.randint(10000000, 99999999)}'
            )
            created_students.append(stu)

        # ==========================================
        # 2. COURSES, SUBJECTS, CHAPTERS
        # ==========================================
        course_jee = Course.objects.create(
            title='JEE Advanced Pinnacle (2-Year Classroom)',
            slug='jee-advanced-pinnacle',
            category='ENGINEERING',
            target_class='Class 11 & 12 / Droppers',
            short_description='Flagship intensive program with Top-50 IITian mentorship, rigorous testing, and advanced problem-solving.',
            description='Designed specifically for ambitious engineering aspirants targeting Top 500 ranks in JEE Main & Advanced. Covers 1000+ hours of live/recorded lectures, daily practice problems, proctored computer-based test series, and dedicated 1-on-1 doubt resolution counters.',
            duration_weeks=104,
            price=75000.00,
            discount_price=59999.00,
            thumbnail_url='https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=80',
            features=[
                '1000+ Hours of Classroom & Recorded Concept Modules',
                'National Ranker Level Daily Practice Problem Sheets (DPPs)',
                'Weekly All-India Computer Based Test Series (AI-CBT)',
                '1-on-1 Personalized Mentor & Doubt Clearing Sessions',
                'Comprehensive Printed Theory & Problem Bank Modules'
            ],
            is_featured=True,
            order=1
        )

        course_neet = Course.objects.create(
            title='NEET-UG Medical Champions (Target 2026/2027)',
            slug='neet-medical-champions',
            category='MEDICAL',
            target_class='Class 11 & 12',
            short_description='Comprehensive AIIMS/NEET preparation with 100% NCERT mastery, 3D anatomical models, and speed workshops.',
            description='Complete medical coaching program led by AIIMS doctor faculty. Special focus on NCERT line-by-line decoding in Biology, high-speed calculation hacks in Physics, and organic mechanism blueprints.',
            duration_weeks=104,
            price=68000.00,
            discount_price=54999.00,
            thumbnail_url='https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=600&auto=format&fit=crop&q=80',
            features=[
                'Complete Line-by-Line NCERT Decoding & Mnemonics',
                '3D Biology Visual Anatomy & Physiology Modules',
                'Physics Numerical Speed & Shortcut Bootcamps',
                '720-Marks Exact Simulation Mock Tests with OMR Analytics',
                'Doctor-guided Mentorship & Counseling Seminars'
            ],
            is_featured=True,
            order=2
        )

        course_found = Course.objects.create(
            title='Foundations & Olympiad Master (Class 9 & 10)',
            slug='foundation-olympiad-master',
            category='FOUNDATION',
            target_class='Class 9 & 10',
            short_description='Build an unbeatable analytical foundation for NTSE, PRMO, NSEJS, and early competitive edge.',
            description='Pre-foundation program designed to cultivate deep scientific curiosity, logical thinking, and competitive readiness starting from Class 9 & 10.',
            duration_weeks=52,
            price=38000.00,
            discount_price=29999.00,
            thumbnail_url='https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&auto=format&fit=crop&q=80',
            features=[
                'Early Conceptual Building in Physics, Chemistry & Math',
                'Olympiad & PRMO Level Problem-Solving Strategies',
                'Mental Ability & Logical Reasoning Special Classes',
                'School Board Exam 100% Score Guarantee Prep'
            ],
            is_featured=True,
            order=3
        )

        course_crash = Course.objects.create(
            title='Fast-Track JEE/NEET 90-Day Crash Course',
            slug='fast-track-crash-course',
            category='CRASH_COURSE',
            target_class='Class 12 / Repeaters',
            short_description='High-yield revision, formula blitz, 5000+ most-probable question drills, and 30 full CBT mocks.',
            description='Intensive last-lap sprint designed to boost your rank by up to 40 percentile with high-yield revision and test-taking strategies.',
            duration_weeks=12,
            price=19999.00,
            discount_price=14999.00,
            thumbnail_url='https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=80',
            features=[
                'High-Yield Formula Blitz & Mind Maps',
                'Top 5000 Most Expected Exam Questions',
                '30 Full Length Timed CBT Mocks with Video Solutions',
                'Doubt Solving via Live Hotline'
            ],
            is_featured=False,
            order=4
        )

        # Subjects for JEE
        sub_phy = Subject.objects.create(
            course=course_jee,
            name='Physics',
            code='PHY-JEE',
            icon='zap',
            color_accent='#3B82F6',
            order=1
        )
        sub_chem = Subject.objects.create(
            course=course_jee,
            name='Chemistry',
            code='CHM-JEE',
            icon='flask-conical',
            color_accent='#10B981',
            order=2
        )
        sub_math = Subject.objects.create(
            course=course_jee,
            name='Mathematics',
            code='MTH-JEE',
            icon='binary',
            color_accent='#F59E0B',
            order=3
        )

        # Subjects for NEET
        sub_bio = Subject.objects.create(
            course=course_neet,
            name='Biology & Genetics',
            code='BIO-NEET',
            icon='dna',
            color_accent='#EC4899',
            order=1
        )
        sub_neet_phy = Subject.objects.create(
            course=course_neet,
            name='Physics for NEET',
            code='PHY-NEET',
            icon='atom',
            color_accent='#3B82F6',
            order=2
        )

        # Chapters for Physics
        ch_rot = Chapter.objects.create(
            subject=sub_phy,
            title='Rotational Motion & Rigid Body Dynamics',
            chapter_number=1,
            description='Moment of Inertia, Torque, Angular Momentum Conservation, Rolling Motion without Slipping.',
            estimated_hours=12.0,
            order=1
        )
        ch_elec = Chapter.objects.create(
            subject=sub_phy,
            title='Electrostatics & Electric Potential',
            chapter_number=2,
            description='Coulomb Law, Gauss Theorem, Electric Potential, Capacitors and Dielectric polarization.',
            estimated_hours=14.0,
            order=2
        )
        ch_opt = Chapter.objects.create(
            subject=sub_phy,
            title='Wave Optics & Interference',
            chapter_number=3,
            description='Huygens Principle, Young Double Slit Experiment, Diffraction, and Polarization.',
            estimated_hours=8.0,
            order=3
        )

        # Chapters for Chemistry
        ch_org = Chapter.objects.create(
            subject=sub_chem,
            title='Aldehydes, Ketones & Carboxylic Acids',
            chapter_number=1,
            description='Nucleophilic addition mechanisms, Cannizzaro, Aldol condensation, Named organic reactions.',
            estimated_hours=10.0,
            order=1
        )
        ch_thermo = Chapter.objects.create(
            subject=sub_chem,
            title='Chemical Thermodynamics & Energetics',
            chapter_number=2,
            description='First and Second Laws of Thermodynamics, Gibbs Free Energy, Spontaneity.',
            estimated_hours=9.0,
            order=2
        )

        # Chapters for Mathematics
        ch_calc = Chapter.objects.create(
            subject=sub_math,
            title='Definite Integration & Areas under Curves',
            chapter_number=1,
            description='Leibnitz Rule, Properties of Definite Integrals, Bounded Area calculations.',
            estimated_hours=11.0,
            order=1
        )
        ch_vec = Chapter.objects.create(
            subject=sub_math,
            title='Vector Algebra & 3D Geometry',
            chapter_number=2,
            description='Dot and Cross Products, Scalar Triple Product, Equations of Lines & Planes in Space.',
            estimated_hours=10.0,
            order=2
        )

        # Chapters for Biology
        ch_gen = Chapter.objects.create(
            subject=sub_bio,
            title='Principles of Inheritance & Molecular Basis',
            chapter_number=1,
            description='Mendelian Genetics, DNA Replication, Transcription, Translation, Lac Operon.',
            estimated_hours=15.0,
            order=1
        )

        # ==========================================
        # 3. VIDEO LESSONS (Hierarchy with Demo URLs)
        # ==========================================
        # Educational sample video embeds
        video_lessons_data = [
            # Rotational Motion
            (
                course_jee, sub_phy, ch_rot, teacher_physics,
                'L1: Introduction to Rigid Bodies & Moment of Inertia of Continuous Bodies',
                'Comprehensive derivation of Moment of Inertia for rods, rings, discs, solid cylinders, and spheres using integration techniques.',
                'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500&auto=format&fit=crop&q=80',
                48, 1, True, True
            ),
            (
                course_jee, sub_phy, ch_rot, teacher_physics,
                'L2: Parallel and Perpendicular Axis Theorems with Advanced Problem Solving',
                'Applications of Parallel Axis Theorem and Perpendicular Axis Theorem on composite 2D and 3D planar geometries.',
                'https://www.youtube.com/embed/kJQP7kiw5Fk',
                'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500&auto=format&fit=crop&q=80',
                52, 2, True, False
            ),
            (
                course_jee, sub_phy, ch_rot, teacher_physics,
                'L3: Torque, Angular Acceleration & Dynamics of Fixed Axis Rotation',
                'Newton second law in rotational form, pulleys with mass, string friction, and toppling conditions.',
                'https://www.youtube.com/embed/L_LUpnjgPso',
                'https://images.unsplash.com/photo-1518152006812-edab29b069ac?w=500&auto=format&fit=crop&q=80',
                55, 3, True, False
            ),
            (
                course_jee, sub_phy, ch_rot, teacher_physics,
                'L4: Rolling Motion without Slipping & Energy Conservation on Inclines',
                'Pure rolling kinematics, instantaneous axis of rotation (IAOR), friction in rolling, and inclined plane motion.',
                'https://www.youtube.com/embed/fJ9rUzIMcZQ',
                'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=500&auto=format&fit=crop&q=80',
                60, 4, True, False
            ),
            # Electrostatics
            (
                course_jee, sub_phy, ch_elec, teacher_physics,
                'L1: Gauss Law & Electric Flux across Complex Gaussian Surfaces',
                'Symmetry arguments, flux through cubes, cylinders, and electric field derivations for continuous charge distributions.',
                'https://www.youtube.com/embed/3JZ_D3ELwOQ',
                'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&auto=format&fit=crop&q=80',
                45, 1, True, True
            ),
            (
                course_jee, sub_phy, ch_elec, teacher_physics,
                'L2: Electrostatic Potential Energy & Self Energy of Charged Shells',
                'Work-energy theorem in electrostatic fields, dipole in uniform/non-uniform fields, and self-energy calculations.',
                'https://www.youtube.com/embed/2Vv-BfVoq4g',
                'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=500&auto=format&fit=crop&q=80',
                50, 2, True, False
            ),
            # Organic Chemistry
            (
                course_jee, sub_chem, ch_org, teacher_chem,
                'L1: Nucleophilic Addition to Carbonyl Groups & Mechanism Deep Dive',
                'Grignard reactions, cyanohydrin formation, acetal and ketal protection strategies.',
                'https://www.youtube.com/embed/9bZkp7q19f0',
                'https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?w=500&auto=format&fit=crop&q=80',
                46, 1, True, True
            ),
            (
                course_jee, sub_chem, ch_org, teacher_chem,
                'L2: Aldol Condensation, Cannizzaro Reaction & Crossed Aldol Tricks',
                'Alpha-hydrogen acidity, enolate ion intermediate, intramolecular aldol and crossed Cannizzaro mechanisms.',
                'https://www.youtube.com/embed/kJQP7kiw5Fk',
                'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=500&auto=format&fit=crop&q=80',
                54, 2, True, False
            ),
            # Mathematics Calculus
            (
                course_jee, sub_math, ch_calc, teacher_maths,
                'L1: Fundamental Theorems of Definite Integrals & King Property',
                'Symmetry rules, Queen property, King property (f(a+b-x)), and integration of periodic functions.',
                'https://www.youtube.com/embed/3JZ_D3ELwOQ',
                'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500&auto=format&fit=crop&q=80',
                50, 1, True, True
            ),
            (
                course_jee, sub_math, ch_calc, teacher_maths,
                'L2: Newton-Leibnitz Rule of Differentiation under the Integral Sign',
                'Differentiating definite integrals with variable limits, limit of sum as definite integral formulation.',
                'https://www.youtube.com/embed/L_LUpnjgPso',
                'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&auto=format&fit=crop&q=80',
                52, 2, True, False
            ),
            # Biology Genetics
            (
                course_neet, sub_bio, ch_gen, teacher_bio,
                'L1: Mendelian Genetics, Incomplete Dominance & Multiple Alleles',
                'Monohybrid and dihybrid crosses, chromosomal theory of inheritance, ABO blood grouping genetics.',
                'https://www.youtube.com/embed/fJ9rUzIMcZQ',
                'https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=500&auto=format&fit=crop&q=80',
                44, 1, True, True
            )
        ]

        created_lessons = []
        for crs, sbj, chp, tch, ttl, desc, v_url, th_url, dur, ord_idx, is_pub, is_free in video_lessons_data:
            vl = VideoLesson.objects.create(
                course=crs,
                subject=sbj,
                chapter=chp,
                teacher=tch,
                title=ttl,
                description=desc,
                video_url=v_url,
                thumbnail_url=th_url,
                duration_minutes=dur,
                order=ord_idx,
                is_published=is_pub,
                is_free_preview=is_free
            )
            created_lessons.append(vl)

        # Record demo progress for Aarav Sharma (student)
        if len(created_lessons) >= 4:
            VideoProgress.objects.create(
                student=demo_student,
                video=created_lessons[0],
                is_completed=True,
                watched_duration_seconds=48 * 60,
                last_position_seconds=48 * 60
            )
            VideoProgress.objects.create(
                student=demo_student,
                video=created_lessons[1],
                is_completed=True,
                watched_duration_seconds=52 * 60,
                last_position_seconds=52 * 60
            )
            VideoProgress.objects.create(
                student=demo_student,
                video=created_lessons[2],
                is_completed=False,
                watched_duration_seconds=30 * 60,
                last_position_seconds=1800
            )

        # ==========================================
        # 4. STUDY MATERIALS & NOTES
        # ==========================================
        StudyMaterial.objects.create(
            course=course_jee,
            subject=sub_phy,
            chapter=ch_rot,
            teacher=teacher_physics,
            title='Rotational Motion Complete Class Notes & Derivation Blueprints (PDF)',
            description='Detailed handwritten lecture notes including all standard Moment of Inertia integrations and rolling friction conditions.',
            material_type='PDF_NOTES',
            file_url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            file_size_mb=4.8,
            download_count=184
        )
        StudyMaterial.objects.create(
            course=course_jee,
            subject=sub_phy,
            chapter=ch_rot,
            teacher=teacher_physics,
            title='Daily Practice Problem (DPP #04) - Advanced Mechanics & Rigid Body Dynamics',
            description='25 high-level multi-correct and matrix-match questions with complete hints and step solutions.',
            material_type='DPP',
            file_url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            file_size_mb=2.1,
            download_count=210
        )
        StudyMaterial.objects.create(
            course=course_jee,
            subject=sub_math,
            chapter=ch_calc,
            teacher=teacher_maths,
            title='Definite Integration Formula Flashcards & Shortcut Cheatsheet',
            description='Quick memory summary containing 40+ standard reduction formulas and Leibnitz variations.',
            material_type='FORMULA_SHEET',
            file_url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            file_size_mb=1.6,
            download_count=340
        )
        StudyMaterial.objects.create(
            course=course_jee,
            subject=sub_chem,
            chapter=ch_org,
            teacher=teacher_chem,
            title='Top 100 Organic Conversions & Named Reactions Handbook',
            description='Master organic chemistry synthesis pathways for JEE Advanced & Boards.',
            material_type='PYQ',
            file_url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            file_size_mb=6.2,
            download_count=415
        )

        # ==========================================
        # 5. BATCHES & ENROLLMENTS
        # ==========================================
        batch_alpha = Batch.objects.create(
            name='JEE Pinnacle Alpha-1 (Class 12)',
            code='BATCH-PINNACLE-A1',
            course=course_jee,
            start_date=datetime.date(2025, 4, 10),
            end_date=datetime.date(2026, 5, 30),
            schedule_time='Mon, Wed, Fri, Sat (4:00 PM - 8:00 PM)',
            classroom='Lecture Hall Alpha-1 (Main Campus)',
            mode='HYBRID',
            max_capacity=45
        )
        batch_alpha.teachers.add(teacher_physics, teacher_chem, teacher_maths)

        batch_medical = Batch.objects.create(
            name='NEET Medical Champions Batch M-1',
            code='BATCH-NEET-M1',
            course=course_neet,
            start_date=datetime.date(2025, 4, 15),
            end_date=datetime.date(2026, 5, 15),
            schedule_time='Tue, Thu, Sat, Sun (3:30 PM - 7:30 PM)',
            classroom='Bio-Med Hall Beta-2',
            mode='OFFLINE',
            max_capacity=50
        )
        batch_medical.teachers.add(teacher_bio, teacher_chem)

        batch_found = Batch.objects.create(
            name='Super-30 Foundation Class 10',
            code='BATCH-FOUND-S30',
            course=course_found,
            start_date=datetime.date(2025, 6, 1),
            end_date=datetime.date(2026, 3, 31),
            schedule_time='Tue, Thu, Sat (5:00 PM - 7:30 PM)',
            classroom='Gamma Seminar Room',
            mode='HYBRID',
            max_capacity=30
        )
        batch_found.teachers.add(teacher_physics, teacher_maths)

        # Enrollments
        for stu in created_students[:4]:
            BatchEnrollment.objects.create(batch=batch_alpha, student=stu, status='ACTIVE')
        for stu in created_students[1:]:
            BatchEnrollment.objects.get_or_create(batch=batch_medical, student=stu, defaults={'status': 'ACTIVE'})

        # ==========================================
        # 6. TESTS, QUESTIONS & ATTEMPTS
        # ==========================================
        test_jee = Test.objects.create(
            title='JEE Advanced All-India Mock Test #01 (Physics & Mechanics)',
            course=course_jee,
            batch=batch_alpha,
            duration_minutes=60,
            total_marks=40,
            passing_marks=16,
            start_time=timezone.now() - datetime.timedelta(days=2),
            end_time=timezone.now() + datetime.timedelta(days=10),
            instructions='1. Total 10 Questions. Each carries 4 Marks.\n2. Negative Marking: -1 Mark for incorrect choice.\n3. Calculators/scratch devices are strictly prohibited.\n4. Click Submit once finished.',
            created_by=teacher_physics,
            is_published=True
        )

        questions_data = [
            (
                'A uniform solid sphere of mass M and radius R rolls without slipping down an inclined plane of inclination θ. What is the acceleration of its center of mass down the plane?',
                '(5/7) g sin θ',
                '(3/5) g sin θ',
                '(2/3) g sin θ',
                '(1/2) g sin θ',
                'A',
                4.0, 1.0,
                'Acceleration of rolling body down incline = (g sin θ) / (1 + I/MR²). For solid sphere, I = 2/5 MR², hence a = (g sin θ) / (1 + 2/5) = (5/7) g sin θ.',
                1
            ),
            (
                'A particle of mass m is moving with constant velocity v along the line y = b. What is the magnitude of its angular momentum with respect to the origin at any instant t?',
                'm v b',
                'm v (x² + b²)^(1/2)',
                'Zero',
                'm v t',
                'A',
                4.0, 1.0,
                'Angular momentum L = r × p = m(r_perp * v). Here the perpendicular distance from origin to the straight line y=b is constantly b, therefore L = m*v*b.',
                2
            ),
            (
                'What is the electric potential at the center of a hemispherical shell of radius R carrying a uniform surface charge density σ?',
                'σ R / (2 ε₀)',
                'σ R / (4 ε₀)',
                'σ R / (ε₀)',
                'Zero',
                'A',
                4.0, 1.0,
                'Every element on the hemisphere is at an equal distance R from the center. V = (1/4πε₀) * Q / R. Here Q = σ * (2πR²). Thus V = (2πR²σ) / (4πε₀R) = σR / (2ε₀).',
                3
            ),
            (
                'If the torque acting on a body about a fixed axis is zero, which of the following quantities must remain constant?',
                'Angular momentum',
                'Angular acceleration',
                'Kinetic energy',
                'Linear velocity',
                'A',
                4.0, 1.0,
                'By Newton second law for rotation, Torque = dL/dt. When Torque = 0, dL/dt = 0, meaning Angular Momentum L remains strictly conserved.',
                4
            ),
            (
                'The value of the definite integral ∫₀^(π/2) (sin x / (sin x + cos x)) dx is equal to:',
                'π / 4',
                'π / 2',
                '1',
                '0',
                'A',
                4.0, 1.0,
                'Let I = ∫₀^(π/2) (sin x / (sin x + cos x)) dx. By King property, I = ∫₀^(π/2) (cos x / (sin x + cos x)) dx. Adding the two: 2I = ∫₀^(π/2) 1 dx = π/2 => I = π/4.',
                5
            )
        ]

        created_questions = []
        for q_txt, op_a, op_b, op_c, op_d, corr, mrk, neg, exp, ord_idx in questions_data:
            q = Question.objects.create(
                test=test_jee,
                question_text=q_txt,
                option_a=op_a,
                option_b=op_b,
                option_c=op_c,
                option_d=op_d,
                correct_option=corr,
                marks=mrk,
                negative_marks=neg,
                explanation=exp,
                order=ord_idx
            )
            created_questions.append(q)

        # Create evaluated attempt for student Aarav Sharma
        attempt = StudentTestAttempt.objects.create(
            student=demo_student,
            test=test_jee,
            start_time=timezone.now() - datetime.timedelta(hours=2),
            submit_time=timezone.now() - datetime.timedelta(hours=1),
            score=16.0,
            total_possible_marks=20.0,
            percentage=80.0,
            is_passed=True,
            status='SUBMITTED'
        )
        for i, q in enumerate(created_questions[:4]):
            selected = 'A' if i != 2 else 'B'
            is_corr = (selected == q.correct_option)
            StudentAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected_option=selected,
                is_correct=is_corr,
                marks_awarded=4.0 if is_corr else -1.0
            )

        # ==========================================
        # 7. ATTENDANCE RECORDS (Past 14 Days)
        # ==========================================
        today = timezone.now().date()
        for day_offset in range(14, -1, -1):
            curr_date = today - datetime.timedelta(days=day_offset)
            if curr_date.weekday() != 6:  # Skip Sunday
                for stu in created_students[:4]:
                    # High present rate
                    stat = 'PRESENT' if (stu.id + day_offset) % 7 != 0 else 'ABSENT'
                    Attendance.objects.create(
                        batch=batch_alpha,
                        student=stu,
                        date=curr_date,
                        status=stat,
                        marked_by=teacher_physics,
                        remarks='Regular class attendance' if stat == 'PRESENT' else 'Informed absence'
                    )

        # ==========================================
        # 8. FEE RECORDS & INVOICES
        # ==========================================
        FeeRecord.objects.create(
            student=demo_student,
            course=course_jee,
            batch=batch_alpha,
            invoice_number='INV-2025-0891',
            title='Class 12 JEE Advanced Pinnacle - Installment 1 (Tuition & Material Kit)',
            total_amount=35000.00,
            paid_amount=35000.00,
            due_date=today - datetime.timedelta(days=60),
            status='PAID',
            payment_mode='UPI',
            payment_date=today - datetime.timedelta(days=62),
            transaction_id='UPI-HDFC-9988221144',
            receipt_url='/api/fees/1/receipt/',
            remarks='Full Term-1 paid with early bird scholarship discount applied.'
        )

        FeeRecord.objects.create(
            student=demo_student,
            course=course_jee,
            batch=batch_alpha,
            invoice_number='INV-2026-1042',
            title='Class 12 JEE Advanced Pinnacle - Installment 2 (Test Series & AI-CBT)',
            total_amount=24999.00,
            paid_amount=0.00,
            due_date=today + datetime.timedelta(days=20),
            status='PENDING',
            remarks='Term-2 Computer Based Test series and Crash booster fee.'
        )

        FeeRecord.objects.create(
            student=created_students[1],
            course=course_neet,
            batch=batch_medical,
            invoice_number='INV-2025-0720',
            title='NEET Medical Champions - Annual Academic Tuition Fee',
            total_amount=54999.00,
            paid_amount=54999.00,
            due_date=today - datetime.timedelta(days=45),
            status='PAID',
            payment_mode='NETBANKING',
            payment_date=today - datetime.timedelta(days=46),
            transaction_id='NEFT-SBI-4433221100',
            remarks='Paid in full.'
        )

        # ==========================================
        # 9. CERTIFICATES
        # ==========================================
        Certificate.objects.create(
            student=demo_student,
            course=course_jee,
            certificate_number='MC-CERT-JEE-2025-014',
            title='Certificate of Academic Distinction & Top Rank in Physics Benchmark',
            issue_date=today - datetime.timedelta(days=30),
            grade='A+ (Outstanding)',
            verification_code=uuid.UUID('c90a5a81-6b01-4aca-bd7c-41b781d94242'),
            description='Awarded to Aarav Sharma for securing 1st Rank in the All-India Physics Benchmark Olympiad conducted across 18 centers of Mayank Classes.',
            certificate_url='/verify-certificate/c90a5a81-6b01-4aca-bd7c-41b781d94242/'
        )

        # ==========================================
        # 10. PORTAL DATA (Notices, Testimonials, Toppers, Gallery, Inquiries)
        # ==========================================
        Notice.objects.create(
            title='All-India JEE Advanced Mock Test Series (AI-CBT #03) Schedule Released',
            category='EXAM',
            target_role='ALL',
            content='The 3rd nationwide Computer Based Mock Test for all Class 12 and Repeater batches will be held on Sunday from 9:00 AM to 12:00 PM in the Digital Exam Lab. Students must arrive with their ID cards.',
            is_pinned=True,
            attachment_url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        )

        Notice.objects.create(
            title='Special Masterclass on Organic Reaction Mechanisms with Dr. Anjali Verma',
            category='EVENT',
            target_role='STUDENT',
            content='Join us for an intensive 3-hour marathon workshop covering every major Named Organic Reaction and electron push mechanisms. Free for all enrolled students.',
            is_pinned=True
        )

        Notice.objects.create(
            title='Independence Day & Janmashtami Academic Holiday Notice',
            category='HOLIDAY',
            target_role='ALL',
            content='The offline institute campus and study libraries will remain closed on the upcoming public holiday. Regular classes will resume as per timetable the following day.',
            is_pinned=False
        )

        # Testimonials
        Testimonial.objects.create(
            student_name='Aditya Singhania',
            course_name='JEE Advanced Pinnacle 2-Year Classroom',
            score_or_rank='AIR 42 (JEE Advanced 2025)',
            college_admitted='IIT Bombay (Computer Science & Engineering)',
            review_text='Mayank Classes transformed my physics and math intuition completely. The faculty here doesn’t just teach formulas; they teach you how to think like an engineer. The AI-CBT test series was harder than the actual JEE exam!',
            rating=5,
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80',
            year=2025,
            is_featured=True
        )

        Testimonial.objects.create(
            student_name='Rhea Deshmukh',
            course_name='NEET Medical Champions Program',
            score_or_rank='AIR 89 (NEET 710/720)',
            college_admitted='AIIMS New Delhi (MBBS)',
            review_text='The line-by-line NCERT decoding sessions and 3D human physiology modules by Dr. Sneha made biology effortless. I scored 355/360 in Biology thanks to their DPP question bank.',
            rating=5,
            avatar_url='https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&auto=format&fit=crop&q=80',
            year=2025,
            is_featured=True
        )

        Testimonial.objects.create(
            student_name='Kunal Kashyap',
            course_name='JEE Super-30 Intensive',
            score_or_rank='AIR 124 (JEE Advanced 2024)',
            college_admitted='IIT Delhi (Electrical Engineering)',
            review_text='The 1-on-1 doubt counters and personalized mentorship by Dr. Rajesh Sharma eliminated every single weak spot I had in mechanics and calculus. Best coaching center in the country!',
            rating=5,
            avatar_url='https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80',
            year=2024,
            is_featured=True
        )

        # Success Stories / Toppers
        SuccessStory.objects.create(
            student_name='Aditya Singhania',
            exam_name='JEE Advanced 2025',
            rank_or_score='All India Rank 42',
            image_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=80',
            summary='2-Year Classroom Student from Kota Center • 100%ile in Physics & Mathematics',
            story='Aditya joined Mayank Classes in Class 11. Through disciplined test analysis, daily DPP solving, and mentor guidance, he scored 326/360 in JEE Advanced 2025 and secured admission in IIT Bombay CS.',
            year=2025,
            is_featured=True
        )

        SuccessStory.objects.create(
            student_name='Rhea Deshmukh',
            exam_name='NEET-UG 2025',
            rank_or_score='AIR 89 • Score 710/720',
            image_url='https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500&auto=format&fit=crop&q=80',
            summary='Classroom Achiever • 355/360 in Biology • Admitted to AIIMS New Delhi',
            story='Rhea consistently topped our All-India CBT tests. Her structured revision of NCERT with Mayank Classes Biology flashcards gave her the speed and confidence to achieve a near-perfect score.',
            year=2025,
            is_featured=True
        )

        SuccessStory.objects.create(
            student_name='Tanmay Bansal',
            exam_name='JEE Main 2025',
            rank_or_score='100.00 Percentile (AIR 14)',
            image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&auto=format&fit=crop&q=80',
            summary='Perfect 300/300 Score in Session 1 • National Olympiad Gold Medalist',
            story='Tanmay solved over 12,000 problems during his 2-year classroom tenure and set a benchmark with 100 percentile in all three subjects.',
            year=2025,
            is_featured=True
        )

        # Gallery
        gallery_items = [
            ('High-Tech Digital Smart Classroom Alpha', 'CAMPUS', 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&auto=format&fit=crop&q=80', 'Air-conditioned acoustic lecture halls equipped with 86-inch interactive 4K displays.'),
            ('Advanced Physics & Optics Research Lab', 'LABS', 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600&auto=format&fit=crop&q=80', 'State-of-the-art laboratory for experimental physics and optics verification.'),
            ('Annual Felicitation Ceremony & Gold Medals 2025', 'AWARDS', 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=600&auto=format&fit=crop&q=80', 'Honoring our Top-100 IIT and AIIMS rankers with scholarships and awards.'),
            ('1-on-1 Personalized Doubt Resolution Arena', 'EVENTS', 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600&auto=format&fit=crop&q=80', 'Faculty available 12 hours a day for individual student mentoring.'),
            ('Central Reference Library & Silent Reading Pods', 'CAMPUS', 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=600&auto=format&fit=crop&q=80', 'Quiet study atmosphere with over 8,000 reference books and high-speed Wi-Fi.'),
            ('National Science Olympiad Felicitation Day', 'AWARDS', 'https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=600&auto=format&fit=crop&q=80', 'Celebrating our Junior Foundation students winning medals at INMO & NSEJS.')
        ]
        for ttl, cat, img, cap in gallery_items:
            GalleryImage.objects.create(title=ttl, category=cat, image_url=img, caption=cap)

        # Contact Inquiries
        ContactInquiry.objects.create(
            full_name='Vikramaditya Rathore',
            email='vikram.rathore@gmail.com',
            phone='+91 98989 11223',
            course_interested='JEE Advanced Pinnacle (2-Year Classroom)',
            current_class='Class 11',
            message='I want to enquire about hostel facilities and scholarship admission tests (MC-SAT) for the 2026 session.',
            status='NEW'
        )
        ContactInquiry.objects.create(
            full_name='Meera Sundaram',
            email='meera.sundaram@yahoo.com',
            phone='+91 97766 55443',
            course_interested='NEET-UG Medical Champions',
            current_class='Class 12',
            message='Seeking weekend crash course and mock test series details.',
            status='CONTACTED',
            notes='Counselor Priya spoke on 24th Aug. Scheduled campus tour for Saturday.'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all realistic demo data for Mayank Classes!'))
        self.stdout.write(self.style.SUCCESS('Demo Logins:'))
        self.stdout.write(self.style.SUCCESS('  Student: student@mayankclasses.com / student123'))
        self.stdout.write(self.style.SUCCESS('  Teacher: teacher@mayankclasses.com / teacher123'))
        self.stdout.write(self.style.SUCCESS('  Admin:   admin@mayankclasses.com   / admin123'))
