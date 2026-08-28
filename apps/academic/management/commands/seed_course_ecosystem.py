import os
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.accounts.models import User
from apps.academic.models import Course, Subject, Chapter, Batch, BatchEnrollment
from apps.lms.models import VideoLesson, StudyMaterial
from apps.portal.models import SuccessStory, Testimonial, Notice, GalleryImage

class Command(BaseCommand):
    help = 'Seeds complete Mayank Classes multi-course ecosystem with Foundation, JEE, NEET, and Other Competitive Exams'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Mayank Classes Course Ecosystem..."))

        # Fetch or create faculty members
        teachers = list(User.objects.filter(role='TEACHER'))
        if not teachers:
            admin_user = User.objects.filter(role='ADMIN').first()
            default_teacher = admin_user
        else:
            default_teacher = teachers[0]

        t_physics = next((t for t in teachers if 'Rajesh' in t.get_full_name() or 'Mayank' in t.get_full_name()), default_teacher)
        t_chem = next((t for t in teachers if 'Anjali' in t.get_full_name()), default_teacher)
        t_math = next((t for t in teachers if 'Vikram' in t.get_full_name()), default_teacher)
        t_bio = next((t for t in teachers if 'Sneha' in t.get_full_name()), default_teacher)

        courses_data = [
            # ==================== 1. FOUNDATION PROGRAMS (CLASSES 6-10) ====================
            {
                'title': 'Class 6 Junior Foundation & Science Olympiad',
                'slug': 'foundation-class-6',
                'category': 'FOUNDATION',
                'target_class': 'Class 6',
                'duration_weeks': 40,
                'mode': 'Classroom Coaching & Interactive Live Online',
                'badge_text': 'EARLY STARTER',
                'price': 28000.00,
                'discount_price': 22500.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=700',
                'short_description': 'Igniting early scientific curiosity, logical reasoning, and school syllabus mastery for NSTSE, NSO & IMO Olympiads.',
                'description': 'Designed specifically for young minds stepping into middle school. This program builds rock-solid basics in Mathematics, General Science, and Mental Ability while empowering students to score top grades in school and compete in national Olympiads.',
                'is_featured': True,
                'order': 1,
                'features': [
                    'Concept-first visual animations & lab kits',
                    'Dedicated Math & Science Olympiad Modules',
                    'Mental Ability & Logical IQ Training',
                    'Weekly Chapter Worksheets & Fun Quizzes',
                    '1-on-1 Teacher Mentorship & School Exam Support'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 6 students aiming to build strong cognitive fundamentals, excel in school CBSE/ICSE exams, and prepare early for competitive Olympiads.',
                    'eligibility': 'Students moving to Class 6 (CBSE, ICSE, or State Boards)',
                    'academic_level': 'School Curriculum + Advanced Olympiad Level (NSO, IMO, NSTSE)',
                    'exam_target': 'Class 6 School Exams, NSO, IMO, NSTSE & SpellBee',
                    'pedagogy': [
                        'Visual Learning: High-impact graphics & daily practical demonstrations',
                        'Active Problem Solving: Daily Math worksheets with step-by-step guidance',
                        'Cognitive Reasoning: Analytical thinking games and logical puzzles',
                        'Continuous Feedback: Monthly Parent-Teacher Progress Meetings'
                    ]
                },
                'faqs': [
                    {'q': 'Will this course burden my child alongside school studies?', 'a': 'Not at all. The course is synchronized with the school academic calendar and requires only 4-6 hours per week.'},
                    {'q': 'Are Olympiad mock tests included in this program?', 'a': 'Yes, students receive 15+ Olympiad-pattern computer-based tests and detailed solution booklets.'},
                    {'q': 'Can students attend online if they miss an offline class?', 'a': 'Yes, all classroom lectures are recorded and accessible anytime on the student LMS app.'}
                ],
                'subjects': [
                    {
                        'name': 'Science (Physics, Chem, Bio)',
                        'code': 'SCI-6',
                        'icon': 'microscope',
                        'color_accent': '#059669',
                        'teacher': t_physics,
                        'chapters': [
                            ('Components of Food & Balanced Diet', 6.0, ['Nutrients & Deficiency Diseases', 'Roughage & Water', 'Dietary Assessment']),
                            ('Light, Shadows & Reflections', 8.0, ['Pinhole Camera', 'Mirrors & Ray Optics Basics', 'Shadow Geometry']),
                            ('Motion & Measurement of Distances', 7.0, ['Standard Units', 'Types of Motion', 'Rectilinear vs Circular Motion']),
                            ('Electricity & Circuits', 8.0, ['Electric Cells', 'Switches & Conductors', 'Simple Bulb Circuit Projects'])
                        ]
                    },
                    {
                        'name': 'Mathematics & Mental Ability',
                        'code': 'MATH-6',
                        'icon': 'calculator',
                        'color_accent': '#4F46E5',
                        'teacher': t_math,
                        'chapters': [
                            ('Knowing Our Numbers & Estimation', 7.0, ['Large Numbers & Place Value', 'Roman Numerals', 'BODMAS & Estimation']),
                            ('Playing with Numbers (HCF & LCM)', 9.0, ['Divisibility Rules', 'Prime Factorization', 'HCF & LCM Word Problems']),
                            ('Integers & Number Line Operations', 8.0, ['Positive & Negative Numbers', 'Addition & Subtraction of Integers', 'Absolute Values']),
                            ('Logical Reasoning & Pattern Analysis', 6.0, ['Series Completion', 'Coding-Decoding', 'Analogy & Venn Diagrams'])
                        ]
                    }
                ]
            },
            {
                'title': 'Class 7 Foundation & Math Wizard Program',
                'slug': 'foundation-class-7',
                'category': 'FOUNDATION',
                'target_class': 'Class 7',
                'duration_weeks': 44,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'OLYMPIAD FOCUS',
                'price': 30000.00,
                'discount_price': 24500.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=700',
                'short_description': 'Strengthening analytical thinking, algebraic foundations, and physics principles for junior competitive exams.',
                'description': 'A comprehensive bridge for Class 7 students focusing on core conceptual clarity. Prepares students for NMTC, IMO, NSO, and establishes early foundations for future JEE/NEET aspirations.',
                'is_featured': False,
                'order': 2,
                'features': [
                    'Algebra & Geometry Visualization workshops',
                    'Advanced Science Lab Demonstrations',
                    'Olympiad Mock Test Series with National Rank',
                    'Daily Practice Problem (DPP) booklets',
                    'Regular doubt-solving counters with IITian faculty'
                ],
                'overview_data': {
                    'who_is_this_for': 'Students in Class 7 eager to develop high-level problem solving and secure top ranks in school and Olympiads.',
                    'eligibility': 'Students entering Class 7',
                    'academic_level': 'School Mastery + National Olympiad Level',
                    'exam_target': 'Class 7 Exams, NMTC, IMO, NSO, Aryabhatta Math Exam',
                    'pedagogy': [
                        'Discovery-Based Math: Exploring formulas through geometric proofs',
                        'Physics Intuition: Experimental setups explaining heat, light, and motion',
                        'Speed & Accuracy: Mental calculation shortcuts and Vedic math tricks'
                    ]
                },
                'faqs': [
                    {'q': 'How does this prepare for JEE/NEET at Class 7 level?', 'a': 'We introduce fundamental concepts in mechanics, numbers, and chemical properties that reappear in Class 11 and 12.'}
                ],
                'subjects': [
                    {
                        'name': 'Science (Physics & Chemistry)',
                        'code': 'SCI-7',
                        'icon': 'atom',
                        'color_accent': '#2563EB',
                        'teacher': t_physics,
                        'chapters': [
                            ('Heat & Temperature Measurement', 7.0, ['Transfer of Heat (Conduction, Convection, Radiation)', 'Thermostats']),
                            ('Acids, Bases and Salts', 8.0, ['Natural Indicators', 'Neutralization Reactions', 'Real-world Applications']),
                            ('Physical & Chemical Changes', 6.0, ['Rusting of Iron', 'Crystallization Process', 'Exothermic vs Endothermic'])
                        ]
                    },
                    {
                        'name': 'Mathematics & Geometry',
                        'code': 'MATH-7',
                        'icon': 'shapes',
                        'color_accent': '#7C3AED',
                        'teacher': t_math,
                        'chapters': [
                            ('Fractions, Decimals & Rational Numbers', 8.0, ['Operations on Rational Numbers', 'Word Problems', 'Number Properties']),
                            ('Simple Equations & Algebraic Expressions', 9.0, ['Linear Equations in 1 Variable', 'Applications to Geometry', 'Transposition Method']),
                            ('Lines, Angles & Triangle Properties', 9.0, ['Parallel Lines & Transversals', 'Pythagoras Property', 'Congruence Criteria'])
                        ]
                    }
                ]
            },
            {
                'title': 'Class 8 Pre-Foundation & IJSO/PRMO Target',
                'slug': 'foundation-class-8',
                'category': 'FOUNDATION',
                'target_class': 'Class 8',
                'duration_weeks': 48,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'PRE-FOUNDATION',
                'price': 34000.00,
                'discount_price': 27500.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=700',
                'short_description': 'The critical springboard for Olympiad aspirants (IJSO, PRMO, NMTC) with rigorous problem-solving in STEM.',
                'description': 'Class 8 is the ideal juncture to introduce formal analytical rigor. This program covers advanced exponents, algebraic identities, mechanics, and organic chemistry basics, laying the bedrock for high school excellence.',
                'is_featured': False,
                'order': 3,
                'features': [
                    'Pre-RMO & Junior Science Olympiad (IJSO) Modules',
                    'Higher-order thinking skills (HOTS) questions',
                    'Computerized CBT diagnostic tests',
                    'Comprehensive printed study modules with theory & exercises',
                    'Dedicated faculty counseling sessions'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 8 students preparing for a leap into senior competitive streams (IIT-JEE / NEET / Olympiads).',
                    'eligibility': 'Students entering Class 8',
                    'academic_level': 'Advanced School + Pre-RMO & IJSO Stage-1',
                    'exam_target': 'Class 8 School Exams, PRMO/IOQM, NSO, IMO, NMTC',
                    'pedagogy': [
                        'Structured Theory → Level-1 School Practice → Level-2 Olympiad HOTS',
                        'Error Analysis: Pinpointing conceptual blind spots in weekly testing'
                    ]
                },
                'faqs': [
                    {'q': 'Is this course suitable for ICSE and State board students?', 'a': 'Yes, our syllabus covers CBSE, ICSE, and advanced competitive topics with universal applicability.'}
                ],
                'subjects': [
                    {
                        'name': 'Physics & Chemistry',
                        'code': 'SCI-8',
                        'icon': 'zap',
                        'color_accent': '#D97706',
                        'teacher': t_physics,
                        'chapters': [
                            ('Force, Pressure & Friction', 9.0, ['Types of Forces', 'Atmospheric Pressure', 'Static vs Dynamic Friction', 'Applications']),
                            ('Sound & Wave Characteristics', 8.0, ['Vibrating Bodies', 'Frequency, Amplitude & Pitch', 'Human Ear Anatomy']),
                            ('Synthetic Materials & Metals', 8.0, ['Reactivity Series', 'Displacement Reactions', 'Corrosion Prevention'])
                        ]
                    },
                    {
                        'name': 'Mathematics & Olympiad Algebra',
                        'code': 'MATH-8',
                        'icon': 'bar-chart-2',
                        'color_accent': '#0284C7',
                        'teacher': t_math,
                        'chapters': [
                            ('Exponents, Powers & Square Roots', 8.0, ['Laws of Exponents', 'Prime Factorization vs Long Division', 'Scientific Notation']),
                            ('Algebraic Expressions & Factorization', 10.0, ['Standard Algebraic Identities', 'Splitting the Middle Term', 'Division of Polynomials']),
                            ('Mensuration & Geometry of 3D Solids', 9.0, ['Surface Areas and Volumes', 'Cylinders, Cones, Cuboids', 'Trapezium & Polygons'])
                        ]
                    }
                ]
            },
            {
                'title': 'Class 9 Foundation Master & NTSE Accelerator',
                'slug': 'foundation-class-9',
                'category': 'FOUNDATION',
                'target_class': 'Class 9',
                'duration_weeks': 52,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'FOUNDATION',
                'price': 38000.00,
                'discount_price': 31000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=700',
                'short_description': 'Master high school physics, chemistry, biology, and math with direct alignment to JEE & NEET foundational curricula.',
                'description': 'Class 9 concepts are 60% of senior JEE/NEET topics (Kinematics, Laws of Motion, Gravitation, Atomic Structure, Coordinate Geometry). This program guarantees 95%+ school marks while accelerating competitive acumen.',
                'is_featured': True,
                'order': 4,
                'features': [
                    'Complete NCERT + Advanced JEE/NEET Foundation coverage',
                    'All-India Test Series (AITS) on Computer Based Testing UI',
                    'Printed Study Packages + Chapter DPP sheets',
                    'Doubt clearing counters with senior Kota faculty',
                    'Regular Parent-Teacher performance review sessions'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 9 students targeting future medical or engineering careers and seeking top grades in high school.',
                    'eligibility': 'Students studying in Class 9',
                    'academic_level': 'CBSE Class 9 + JEE Main & NEET Foundations',
                    'exam_target': 'Class 9 School Finals, NTSE Stage-1, IOQM, NSO, IMO',
                    'pedagogy': [
                        'Derivation-Oriented Learning: Understanding physics mechanics equations from graphs',
                        'Micro-Concept Drills: 20 DPP questions after every classroom lecture'
                    ]
                },
                'faqs': [
                    {'q': 'How will this help with Class 10 Boards next year?', 'a': 'Class 9 concepts form the mathematical and scientific spine for Class 10. Students entering 10th with this foundation find Boards effortless.'}
                ],
                'subjects': [
                    {
                        'name': 'Physics',
                        'code': 'PHY-9',
                        'icon': 'activity',
                        'color_accent': '#E11D48',
                        'teacher': t_physics,
                        'chapters': [
                            ('Motion in a Straight Line', 10.0, ['Distance & Displacement', 'Speed vs Velocity', 'Equations of Motion (Graphical & Calculus)', 'Acceleration Graphs']),
                            ('Force and Newton\'s Laws of Motion', 12.0, ['Inertia & Momentum', 'Second Law Derivation F=ma', 'Conservation of Momentum', 'FBD Basics']),
                            ('Gravitation & Fluid Mechanics', 10.0, ['Universal Law of Gravitation', 'Free Fall & Acceleration g', 'Buoyancy & Archimedes Principle', 'Relative Density']),
                            ('Work, Energy and Power', 8.0, ['Work Done by Force', 'Kinetic & Potential Energy', 'Law of Conservation of Energy', 'Commercial Unit of Energy'])
                        ]
                    },
                    {
                        'name': 'Chemistry',
                        'code': 'CHEM-9',
                        'icon': 'flask',
                        'color_accent': '#059669',
                        'teacher': t_chem,
                        'chapters': [
                            ('Matter in Our Surroundings', 7.0, ['States of Matter', 'Evaporation & Latent Heat', 'Sublimation']),
                            ('Is Matter Around Us Pure?', 8.0, ['Solutions, Suspensions & Colloids', 'Separation Techniques', 'Physical vs Chemical Changes']),
                            ('Atoms and Molecules', 10.0, ['Laws of Chemical Combination', 'Mole Concept & Molar Mass', 'Writing Chemical Formulae']),
                            ('Structure of the Atom', 9.0, ['Thomson, Rutherford & Bohr Models', 'Valency & Electronic Configuration', 'Isotopes & Isobars'])
                        ]
                    },
                    {
                        'name': 'Mathematics',
                        'code': 'MATH-9',
                        'icon': 'divide',
                        'color_accent': '#4F46E5',
                        'teacher': t_math,
                        'chapters': [
                            ('Number Systems & Real Numbers', 8.0, ['Irrational Numbers', 'Real Numbers & Operations', 'Rationalizing the Denominator', 'Laws of Exponents']),
                            ('Polynomials & Algebraic Identities', 12.0, ['Zeros of Polynomial', 'Remainder & Factor Theorems', 'Factorization of Cubics', 'Algebraic Identities']),
                            ('Coordinate Geometry & Linear Equations', 8.0, ['Cartesian Plane', 'Graph of 2-Variable Equations', 'Slope & Intercept Basics']),
                            ('Triangles, Circles & Quadrilaterals', 12.0, ['Congruence Criteria', 'Circle Theorems & Chords', 'Cyclic Quadrilaterals'])
                        ]
                    }
                ]
            },
            {
                'title': 'Class 10 Board Excellence & JEE/NEET Bridge',
                'slug': 'foundation-class-10',
                'category': 'FOUNDATION',
                'target_class': 'Class 10',
                'duration_weeks': 52,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'BOARD + FOUNDATION',
                'price': 42000.00,
                'discount_price': 34500.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=700',
                'short_description': 'Score 98%+ in Class 10 Board Examinations while building seamless conceptual bridges for 11th & 12th JEE/NEET.',
                'description': 'The definitive Class 10 master program. Combines complete Board syllabus mastery with early Class 11 bridge topics (Trigonometry, Kinematics, Chemical Bonding, Genetics), ensuring students start Class 11 far ahead of their national peers.',
                'is_featured': True,
                'order': 5,
                'features': [
                    '100% Board Exam Syllabus Mastery + Sample Papers',
                    'Early JEE/NEET Bridge Modules (Class 11 Preview)',
                    'Previous 10 Years Board Papers solved line-by-line',
                    'Full-Syllabus Board Mock Tests with subjective grading',
                    'Special NTSE & Olympiad Advanced Workshops'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 10 students determined to top their Board exams while creating a dominant head-start for IIT-JEE and NEET.',
                    'eligibility': 'Students studying in Class 10',
                    'academic_level': 'Class 10 Board Syllabus + Level-1 JEE/NEET Bridge',
                    'exam_target': 'CBSE/ICSE Class 10 Boards, NTSE, IOQM, Early JEE/NEET Bridge',
                    'pedagogy': [
                        'Dual-Track Learning: Board Answer Writing Rigor + Objective Competitive Speed',
                        'Subjective Answer Polishing: Expert evaluation of 5-mark and case-study questions'
                    ]
                },
                'faqs': [
                    {'q': 'Will competitive preparation compromise my Board exam percentage?', 'a': 'No. Our curriculum is mapped directly to NCERT and Board patterns. In 2025, 94% of our Class 10 students scored above 95% in Boards.'},
                    {'q': 'When do we begin the Class 11 Bridge topics?', 'a': 'Bridge concepts are integrated naturally after completing each board chapter (e.g. advanced Trigonometry right after 10th Trig).'}
                ],
                'subjects': [
                    {
                        'name': 'Physics & Chemistry',
                        'code': 'SCI-10',
                        'icon': 'zap',
                        'color_accent': '#DC2626',
                        'teacher': t_physics,
                        'chapters': [
                            ('Light: Reflection and Refraction', 11.0, ['Spherical Mirrors & Ray Diagrams', 'Lens Formula & Magnification', 'Refractive Index & Snell\'s Law']),
                            ('Electricity & Magnetic Effects of Current', 13.0, ['Ohm\'s Law & Resistors in Series/Parallel', 'Electric Power & Heating Effect', 'Magnetic Field Lines', 'Electromagnetic Induction']),
                            ('Chemical Reactions & Equations', 8.0, ['Balancing Equations', 'Types of Reactions', 'Oxidation-Reduction & Corrosion']),
                            ('Carbon and Its Compounds', 12.0, ['Covalent Bonding', 'Versatile Nature of Carbon', 'Homologous Series & IUPAC Nomenclature', 'Soaps & Detergents'])
                        ]
                    },
                    {
                        'name': 'Mathematics',
                        'code': 'MATH-10',
                        'icon': 'percent',
                        'color_accent': '#2563EB',
                        'teacher': t_math,
                        'chapters': [
                            ('Quadratic Equations & Arithmetic Progressions', 10.0, ['Nature of Roots & Formula', 'Word Problems', 'nth Term & Sum of AP', 'Bridge to Series']),
                            ('Introduction to Trigonometry & Applications', 14.0, ['Trigonometric Ratios & Identities', 'Heights and Distances', 'Bridge to Class 11 Compound Angles']),
                            ('Coordinate Geometry & Circles', 9.0, ['Distance & Section Formulae', 'Area of Triangle', 'Tangents to a Circle & Proofs']),
                            ('Statistics & Probability', 8.0, ['Mean, Median, Mode of Grouped Data', 'Ogive Curves', 'Theoretical Probability'])
                        ]
                    }
                ]
            },

            # ==================== 2. JEE PREPARATION ====================
            {
                'title': 'JEE Advanced Pinnacle (2-Year Comprehensive)',
                'slug': 'jee-advanced-pinnacle',
                'category': 'ENGINEERING',
                'target_class': 'Class 11 & 12',
                'duration_weeks': 104,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'IIT FOCUSED',
                'price': 95000.00,
                'discount_price': 82000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=700',
                'short_description': 'Flagship 2-year intensive program for IIT-JEE Main & Advanced led by Kota & Delhi HODs.',
                'description': 'Our most revered classroom coaching ecosystem designed to convert high school students into top 100 All India Rankers. Covers complete Class 11 and 12 Physics, Chemistry, and Mathematics from fundamentals to Irodov, Pathfinder, and Advanced Olympiad level.',
                'is_featured': True,
                'order': 6,
                'features': [
                    'Daily 4 Hours Interactive Lectures with IITian Master Faculty',
                    'Daily Practice Problem (DPP) sets with video solutions',
                    'Fortnightly NTA CBT Mock Tests with Speed & Accuracy Analytics',
                    'Comprehensive 24-Booklet Color Study Material Package',
                    '12-Hour Daily Offline & Online Faculty Doubt Counters',
                    'Personalized 1-on-1 Mentor Allocation for Rank Optimization'
                ],
                'overview_data': {
                    'who_is_this_for': 'Students entering Class 11 aspiring to secure seats in top IITs (IIT Bombay, Delhi, Madras, Kanpur, Kharagpur, Roorkee, etc.).',
                    'eligibility': 'Students moving from Class 10 to Class 11 (Science PCM)',
                    'academic_level': 'NCERT Mastery + JEE Main + JEE Advanced Elite',
                    'exam_target': 'IIT-JEE Advanced, JEE Main, BITSAT, IISER, IAT',
                    'pedagogy': [
                        'Phase 1: First-Principle Conceptual Foundations',
                        'Phase 2: High-Volume Graded Problem Solving (Easy → Medium → Advanced)',
                        'Phase 3: Real CBT Simulation under NTA Pressure',
                        'Phase 4: Targeted Weakness Eradication with Personal Mentors'
                    ]
                },
                'faqs': [
                    {'q': 'What is the batch size for JEE Advanced Pinnacle?', 'a': 'Batches are limited to 30-35 students to guarantee individual attention and personal doubt clearance.'},
                    {'q': 'How are Board exam preparations handled alongside JEE?', 'a': 'Our curriculum integrates NCERT line-by-line along with special Board writing test sessions in Class 12.'},
                    {'q': 'What scholarship opportunities are available?', 'a': 'Students can appear for the Mayank Classes Scholarship Aptitude Test (MC-SAT) to win up to 100% tuition fee waiver.'}
                ],
                'subjects': [
                    {
                        'name': 'Physics for JEE Advanced',
                        'code': 'PHY-JEE',
                        'icon': 'zap',
                        'color_accent': '#3B82F6',
                        'teacher': t_physics,
                        'chapters': [
                            ('Kinematics 1D & 2D (Calculus Approach)', 14.0, ['Calculus in Kinematics', 'Projectile Motion on Inclined Plane', 'Relative Velocity & River Swimmer Problems', 'Constraint Equations']),
                            ('Newton\'s Laws of Motion & Friction', 16.0, ['FBD of Pulley Systems', 'Pseudo Forces & Non-Inertial Frames', 'Static & Kinetic Friction Constraints', 'Circular Motion Dynamics']),
                            ('Work, Power & Energy + Conservation Laws', 14.0, ['Work-Energy Theorem in Variable Fields', 'Potential Energy Curves & Stability', 'Vertical Circular Motion', 'Collisions & Impulse']),
                            ('Rotational Mechanics & Rigid Body Dynamics', 20.0, ['Moment of Inertia of Complex Bodies', 'Torque & Angular Momentum Conservation', 'Rolling Motion with Friction', 'Toppling vs Sliding Dynamics']),
                            ('Electromagnetism & Wave Optics', 22.0, ['Gauss Law & Electrostatic Potential', 'Ampere\'s Circuital Law & Biot-Savart', 'Electromagnetic Induction & Lenz Law', 'Interference & Diffraction'])
                        ]
                    },
                    {
                        'name': 'Chemistry (Physical, Organic & Inorganic)',
                        'code': 'CHEM-JEE',
                        'icon': 'flask',
                        'color_accent': '#10B981',
                        'teacher': t_chem,
                        'chapters': [
                            ('Mole Concept & Stoichiometry', 10.0, ['Limiting Reagent & Yield Calculations', 'Equivalent Weight & Normality', 'Redox Titrations & Iodometry']),
                            ('Atomic Structure & Quantum Numbers', 12.0, ['Bohr Model Limitations', 'de Broglie Wavelength & Heisenberg Principle', 'Schrodinger Wave Equation & Orbitals']),
                            ('Chemical Thermodynamics & Thermochemistry', 14.0, ['First Law & Enthalpy Calculations', 'Entropy & Gibbs Free Energy Criteria', 'Carnot Cycle & Spontaneity']),
                            ('General Organic Chemistry (GOC) & Reaction Mechanisms', 18.0, ['Inductive, Mesomeric & Hyperconjugation Effects', 'Carbocation, Carbanion & Radical Stabilities', 'Electrophilic & Nucleophilic Additions/Substitutions']),
                            ('Coordination Compounds & Periodic Trends', 16.0, ['Crystal Field Theory (CFT)', 'Isomerism in Coordination Complexes', 'Spectrochemical Series & Magnetic Moments'])
                        ]
                    },
                    {
                        'name': 'Mathematics for JEE Advanced',
                        'code': 'MATH-JEE',
                        'icon': 'divide',
                        'color_accent': '#8B5CF6',
                        'teacher': t_math,
                        'chapters': [
                            ('Functions, Limits & Continuity', 16.0, ['Domain & Range of Advanced Functions', 'L\'Hopital Rule & Expansion Methods', 'Continuity & Differentiability Theorems']),
                            ('Differential Calculus & Applications of Derivatives', 18.0, ['Monotonicity & Tangent/Normals', 'Maxima & Minima Optimization', 'Rolle\'s & Lagrange\'s Mean Value Theorems']),
                            ('Integral Calculus (Definite & Indefinite)', 20.0, ['Standard Substitution & By Parts Techniques', 'Properties of Definite Integrals', 'Leibniz Integral Rule', 'Area Under Curves']),
                            ('Coordinate Geometry: Conic Sections', 22.0, ['Parabola, Ellipse & Hyperbola Standard Equations', 'Tangents, Normals & Director Circles', 'Focal Properties & Reflection Principles']),
                            ('Vectors & 3-Dimensional Geometry', 16.0, ['Dot, Cross & Scalar Triple Products', 'Vector Equations of Lines and Planes', 'Shortest Distance Between Skew Lines'])
                        ]
                    }
                ]
            },
            {
                'title': 'JEE Main Target (1-Year Fast-Track)',
                'slug': 'jee-main-target',
                'category': 'ENGINEERING',
                'target_class': 'Class 12',
                'duration_weeks': 52,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'NTA JEE TARGET',
                'price': 68000.00,
                'discount_price': 56000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=700',
                'short_description': 'High-yield 1-year targeted program engineered for maximum percentile in JEE Main Session 1 & 2.',
                'description': 'Engineered specifically for Class 12 students to master high-frequency JEE Main topics, speed-accuracy techniques, and past 10 years NTA question patterns while securing top scores in 12th Board examinations.',
                'is_featured': False,
                'order': 7,
                'features': [
                    'Complete 11th Revision + Intensive 12th Syllabus Coaching',
                    '30+ Full-Syllabus NTA Pattern CBT Mock Tests',
                    'Formula Revision Sheets & Shortcut Tricks handbook',
                    'Daily Question Banks with step-by-step solutions',
                    'Personalized Percentile Predictor & Mentorship'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 12 students aiming for 99+ percentile in JEE Main to secure top branches at NITs, IIITs, and DTU/NSUT.',
                    'eligibility': 'Students entering Class 12 (PCM)',
                    'academic_level': 'JEE Main & 12th Board Excellence',
                    'exam_target': 'JEE Main (January & April Sessions), BITSAT, State Entrances',
                    'pedagogy': [
                        'High-Yield Weightage Focus: Targeting top 60 scoring topics first',
                        'Speed Mastery: Solving standard 25 questions in 45 minutes with precision'
                    ]
                },
                'faqs': [
                    {'q': 'Does this cover Class 11 syllabus revision?', 'a': 'Yes, 40% of the course duration is dedicated to structured Class 11 revision and high-weightage topics.'}
                ],
                'subjects': [
                    {
                        'name': 'Physics (Main Express)',
                        'code': 'PHY-JM',
                        'icon': 'zap',
                        'color_accent': '#2563EB',
                        'teacher': t_physics,
                        'chapters': [
                            ('Current Electricity & Magnetism', 12.0, ['Kirchhoff\'s Laws', 'Potentiometer & Meter Bridge', 'Magnetic Force on Moving Charges']),
                            ('Modern Physics & Semiconductors', 10.0, ['Photoelectric Effect', 'Bohr Model & Nuclear Physics', 'p-n Junction Diodes & Logic Gates'])
                        ]
                    },
                    {
                        'name': 'Mathematics (Main Express)',
                        'code': 'MATH-JM',
                        'icon': 'divide',
                        'color_accent': '#7C3AED',
                        'teacher': t_math,
                        'chapters': [
                            ('Matrices & Determinants', 8.0, ['Properties of Determinants', 'Inverse Matrix & System of Equations', 'Cayley-Hamilton Theorem']),
                            ('Probability & Statistics', 8.0, ['Bayes Theorem', 'Binomial Distribution', 'Standard Deviation & Variance'])
                        ]
                    }
                ]
            },
            {
                'title': 'JEE Droppers / Repeater Super Ranker Batch',
                'slug': 'jee-dropper-rankers',
                'category': 'ENGINEERING',
                'target_class': 'Droppers / 12th Passed',
                'duration_weeks': 44,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'TOP RANKERS',
                'price': 78000.00,
                'discount_price': 64000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=700',
                'short_description': 'Rigorous 10-month rank-elevation program for JEE repeaters aiming to jump into top IIT/NIT percentiles.',
                'description': 'Designed exclusively for repeaters who want a relentless, structured system to fix their weaknesses, eliminate negative marking, and achieve a 99.5+ percentile in JEE Main & Advanced.',
                'is_featured': True,
                'order': 8,
                'features': [
                    'Complete 11th & 12th Syllabus in 350+ Intensive Masterclasses',
                    '50+ All-India CBT Test Series with percentile benchmarking',
                    'Daily 100 Question Sprint Challenge with instant ranking',
                    'Dedicated Droppers Doubt Desk open 8 AM to 9 PM',
                    'Special Advanced Problem Solving sessions with Mayank Sir'
                ],
                'overview_data': {
                    'who_is_this_for': '12th passed students taking a focused drop year to crack IIT-JEE with a single-minded determination.',
                    'eligibility': '12th Passed / Droppers (PCM)',
                    'academic_level': 'Comprehensive JEE Main + Advanced Mastery',
                    'exam_target': 'JEE Main & Advanced 2026',
                    'pedagogy': [
                        'Error Diagnostics: Analyzing previous year failure points and exam temperament',
                        'High-Intensity Practice: 5000+ handpicked multi-concept problems solved under timed constraints'
                    ]
                },
                'faqs': [
                    {'q': 'When do dropper batches start?', 'a': 'Batches start in May, June, and July following Board and JEE results.'}
                ],
                'subjects': [
                    {
                        'name': 'Advanced Problem Solving (PCM)',
                        'code': 'PCM-DROP',
                        'icon': 'target',
                        'color_accent': '#B91C1C',
                        'teacher': t_physics,
                        'chapters': [
                            ('Mechanics & Rotational Mastery', 16.0, ['Advanced Multi-Body Dynamics', 'Impulsive Torques', 'Gyroscope & Precision Motion']),
                            ('Electro-Magnetism & Modern Physics Blitz', 18.0, ['Complex AC Circuits', 'Maxwell Equations & EM Waves', 'Matter Waves & Quantum Numbers']),
                            ('Advanced Integral & Conics Solving', 18.0, ['Definite Integral Inequalities', 'Coaxial Circles & Common Tangents', '3D Analytical Vectors'])
                        ]
                    }
                ]
            },

            # ==================== 3. NEET PREPARATION ====================
            {
                'title': 'NEET-UG Medical Champions (2-Year Comprehensive)',
                'slug': 'neet-medical-champions',
                'category': 'MEDICAL',
                'target_class': 'Class 11 & 12',
                'duration_weeks': 104,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'MOST POPULAR',
                'price': 92000.00,
                'discount_price': 79000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=700',
                'short_description': 'Premier 2-year classroom and online program designed to produce top AIIMS & Government Medical College selections.',
                'description': 'Our celebrated flagship medical program. Comprehensive line-by-line NCERT mastery in Biology (Botany & Zoology), conceptual Physics problem solving, and Physical/Organic/Inorganic Chemistry with doctors and senior medical faculty mentors.',
                'is_featured': True,
                'order': 9,
                'features': [
                    'Daily 4 Hours Lectures by Senior Medical Faculty & AIIMS Mentors',
                    'Line-by-Line NCERT Biology Decoding & 3D Interactive Diagrams',
                    'Physics Simplified for Medical Aspirants (Zero Calculus Anxiety)',
                    'Weekly OMR & Computerized NEET Mock Tests with Negative Marking Analytics',
                    '20000+ Question Bank specifically tuned to NTA NEET pattern',
                    'Special revision workshops and NCERT audio podcasts for memorization'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 11 medical aspirants aiming for 680+ marks in NEET-UG to secure MBBS admission in top AIIMS and Government Medical Colleges.',
                    'eligibility': 'Students moving from Class 10 to Class 11 (PCB)',
                    'academic_level': 'NCERT Line-by-Line + NEET-UG All-India Mastery',
                    'exam_target': 'NEET-UG, AIIMS, JIPMER, State Medical Quota',
                    'pedagogy': [
                        'NCERT Centricity: Every diagram, table, and line in NCERT converted into MCQ drills',
                        'Physics for Doctors: Visual, intuitive problem solving with minimal complex maths',
                        'Spaced Repetition: Retaining thousands of biological taxonomies, cycles, and drug names'
                    ]
                },
                'faqs': [
                    {'q': 'How does Mayank Classes help biology students with Physics?', 'a': 'We teach Physics with visual models and simplified mathematical shortcuts specially tailored for medical students.'},
                    {'q': 'Are biological practical diagrams and experiments covered?', 'a': 'Yes, full practical and experimental syllabus updated as per latest NTA guidelines is taught with 3D animations.'}
                ],
                'subjects': [
                    {
                        'name': 'Biology (Botany & Zoology)',
                        'code': 'BIO-NEET',
                        'icon': 'heart-pulse',
                        'color_accent': '#059669',
                        'teacher': t_bio,
                        'chapters': [
                            ('Cell: The Unit of Life & Cell Cycle', 12.0, ['Prokaryotic vs Eukaryotic Cells', 'Cell Organelles Structure & Function', 'Mitosis, Meiosis & Checkpoints']),
                            ('Plant Physiology & Photosynthesis', 14.0, ['Transport in Plants & Mineral Nutrition', 'Light & Dark Reactions (C3, C4, CAM Cycles)', 'Respiration in Plants & ATP Yield']),
                            ('Human Physiology: Digestion to Neural Control', 22.0, ['Circulatory System & Cardiac Cycle', 'Excretory Products & Nephron Physiology', 'Neural Coordination & Synaptic Transmission', 'Endocrine Hormones & Feedback']),
                            ('Genetics & Molecular Basis of Inheritance', 18.0, ['Mendelian Ratios & Non-Mendelian Genetics', 'DNA Replication, Transcription & Translation', 'Human Genome Project & DNA Fingerprinting', 'Genetic Disorders']),
                            ('Ecology, Biodiversity & Conservation', 12.0, ['Population Interactions & Exponential Growth', 'Ecosystem Energy Flow & Pyramids', 'Biodiversity Hotspots & Conservation Laws'])
                        ]
                    },
                    {
                        'name': 'Physics for NEET',
                        'code': 'PHY-NEET',
                        'icon': 'activity',
                        'color_accent': '#DC2626',
                        'teacher': t_physics,
                        'chapters': [
                            ('Mechanics & Laws of Motion for NEET', 14.0, ['Units & Dimensions', 'Kinematics Formulas & Graphs', 'Newton\'s Laws & Friction Tricks', 'Work Energy Power']),
                            ('Thermodynamics & Kinetic Theory', 10.0, ['Laws of Thermodynamics & Carnot Engine', 'Specific Heat Capacities', 'Kinetic Gas Theory & RMS Velocity']),
                            ('Electrostatics & Current Electricity', 14.0, ['Coulomb Law & Electric Fields', 'Capacitors in Series/Parallel', 'Kirchhoff Laws & Heating Effects of Current']),
                            ('Optics & Modern Physics', 16.0, ['Ray Optics & Optical Instruments', 'Wave Optics & Interference', 'Dual Nature of Radiation & Nuclear Physics'])
                        ]
                    },
                    {
                        'name': 'Chemistry for NEET',
                        'code': 'CHEM-NEET',
                        'icon': 'flask',
                        'color_accent': '#7C3AED',
                        'teacher': t_chem,
                        'chapters': [
                            ('Physical Chemistry & Chemical Equilibrium', 14.0, ['Mole Concept & Redox', 'Ionic Equilibrium & pH Calculations', 'Chemical Kinetics & Rate Laws']),
                            ('Organic Chemistry: Carbonyls to Biomolecules', 18.0, ['Alkanes, Alkenes, Alkynes Reactions', 'Aldehydes, Ketones & Carboxylic Acids', 'Biomolecules (Proteins, Lipids, Nucleic Acids)']),
                            ('Inorganic Chemistry & Periodic Table', 14.0, ['p-Block & d-Block Elements', 'Coordination Chemistry', 'Environmental Chemistry & Qualitative Analysis'])
                        ]
                    }
                ]
            },
            {
                'title': 'NEET Droppers / Repeaters Intensive Repeater Batch',
                'slug': 'neet-dropper-achievers',
                'category': 'MEDICAL',
                'target_class': 'Droppers / 12th Passed',
                'duration_weeks': 44,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'AIIMS TARGET',
                'price': 76000.00,
                'discount_price': 62000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=700',
                'short_description': 'Relentless score-booster batch for repeaters aiming to leap from 500 to 680+ marks in NEET 2026.',
                'description': 'Engineered to turn previous near-misses into assured top-tier Government MBBS seats. Complete 11th & 12th syllabus mapped to 100+ OMR full tests and daily NCERT speed drills.',
                'is_featured': True,
                'order': 10,
                'features': [
                    'Complete 11th & 12th PCB in 400+ targeted masterclasses',
                    '75+ Full-Length NEET OMR Mock Tests with instant All-India Rank',
                    'Personal Mentor for score analysis and negative mark reduction',
                    'Daily 180-Question Sprint Simulations matching NEET 2 PM - 5:20 PM time window',
                    'Dedicated hostel study pods and 24/7 faculty doubt support'
                ],
                'overview_data': {
                    'who_is_this_for': 'NEET repeaters with a passion to crack MBBS with a high rank and secure government medical colleges.',
                    'eligibility': '12th Passed / NEET Repeaters (PCB)',
                    'academic_level': 'Comprehensive NEET Speed & Precision Mastery',
                    'exam_target': 'NEET-UG 2026',
                    'pedagogy': [
                        'Exam Conditioning: Testing repeatedly in the exact 2:00 PM to 5:20 PM slot to match biological clock',
                        'Zero-Negative Challenge: Training students to eliminate doubtful guesses and maximize accuracy'
                    ]
                },
                'faqs': [
                    {'q': 'How many tests will I write in this dropper batch?', 'a': 'You will complete 75+ full-length tests and 150+ chapter-wise diagnostic tests throughout the session.'}
                ],
                'subjects': [
                    {
                        'name': 'Intensive PCB High-Yield Review',
                        'code': 'PCB-DROP',
                        'icon': 'target',
                        'color_accent': '#059669',
                        'teacher': t_bio,
                        'chapters': [
                            ('Complete NCERT Biology High-Speed Drills', 20.0, ['Taxonomy to Biotechnology Fast Recall', 'Diagram Labeling Mastery', 'Assertion-Reason Techniques']),
                            ('Physics 45-Question Rapid Solving', 16.0, ['Formula-to-Answer Speed Drills', 'Dimensional Analysis Shortcuts', 'Error Elimination in Mechanics']),
                            ('Chemistry 180 Marks Strategy', 16.0, ['Direct NCERT Inorganic Lines', 'Name Reactions Flowcharts', 'Equilibrium & Electrochemistry Formulas'])
                        ]
                    }
                ]
            },

            # ==================== 4. OTHER COMPETITIVE & ENTRANCE EXAMS ====================
            {
                'title': 'CUET (UG) General Aptitude + Domain Subjects Prep',
                'slug': 'cuet-ug-master',
                'category': 'OTHER_EXAMS',
                'target_class': 'Class 12 / Passed',
                'duration_weeks': 24,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'CENTRAL UNIS',
                'price': 32000.00,
                'discount_price': 25000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=700',
                'short_description': 'Target top Central Universities (DU, BHU, JNU, Allahabad Univ) with Section I, II & III mastery.',
                'description': 'Comprehensive preparation for Common University Entrance Test (CUET UG) covering English Language, General Test (Numerical Ability, Reasoning, GK/Current Affairs), and Science Domain Subjects.',
                'is_featured': True,
                'order': 11,
                'features': [
                    'Section I: English Comprehension, Vocabulary & Grammar Mastery',
                    'Section II: Domain Subjects (Physics, Chemistry, Maths, Biology) mapped to Class 12 NCERT',
                    'Section III: Quantitative Aptitude, Logical Reasoning & Current Affairs',
                    '25+ CBT Mock Tests simulating NTA CUET Computer Testing Interface',
                    'College & Course Selection Guidance for Delhi University & Central Unis'
                ],
                'overview_data': {
                    'who_is_this_for': 'Class 12 students aiming for top courses (B.Sc, B.Com, B.A, B.Tech) in Delhi University (DU), BHU, JNU, and other premier central universities.',
                    'eligibility': 'Class 12 appearing or passed students',
                    'academic_level': 'Class 12 NCERT + NTA CUET CBT Format',
                    'exam_target': 'CUET (UG) 2026',
                    'pedagogy': [
                        'Speed-Focused CBT drills for 50 questions in 45 minutes',
                        'Comprehensive General Test & English Grammar vocabulary building'
                    ]
                },
                'faqs': [
                    {'q': 'Can I choose my specific domain subjects?', 'a': 'Yes, students can customize their domain package (PCM, PCB, Commerce, or Humanities).'}
                ],
                'subjects': [
                    {
                        'name': 'Section III: General Test & Section I: English',
                        'code': 'CUET-GEN',
                        'icon': 'globe',
                        'color_accent': '#0284C7',
                        'teacher': t_math,
                        'chapters': [
                            ('Numerical Ability & Quantitative Reasoning', 10.0, ['Percentages, Profit & Loss', 'Ratio & Proportion', 'Time, Speed & Distance', 'Data Interpretation']),
                            ('Logical & Analytical Reasoning', 8.0, ['Blood Relations, Direction Sense', 'Seating Arrangements', 'Puzzles & Syllogisms']),
                            ('English Reading Comprehension & Verbal Ability', 8.0, ['Reading Passages', 'Synonyms & Antonyms', 'Sentence Correction', 'Idioms & Phrases'])
                        ]
                    }
                ]
            },
            {
                'title': 'NDA & NA Defence Entrance Comprehensive',
                'slug': 'nda-defence-mastery',
                'category': 'OTHER_EXAMS',
                'target_class': 'Class 11 & 12 / Passed',
                'duration_weeks': 36,
                'mode': 'Classroom Coaching & Live Hybrid',
                'badge_text': 'DEFENCE ENTRANCE',
                'price': 45000.00,
                'discount_price': 36000.00,
                'thumbnail_url': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=700',
                'short_description': 'UPSC National Defence Academy (NDA/NA) Written Exam + SSB Interview Guidance Program.',
                'description': 'Specialized training for UPSC NDA written examination covering Mathematics (300 Marks) and General Ability Test (GAT - 600 Marks: English, Physics, Chemistry, General Science, History, Geography, Current Affairs), coupled with foundational SSB psychological orientation.',
                'is_featured': True,
                'order': 12,
                'features': [
                    'Complete UPSC NDA Mathematics (Algebra, Trig, Calculus, Vectors)',
                    'General Ability Test (GAT) English + Science + GK & Defense Awareness',
                    'Previous 15 Years NDA Question Papers with in-depth solutions',
                    'SSB Interview screening & psychological testing orientation',
                    'Physical fitness guidance and officer personality development'
                ],
                'overview_data': {
                    'who_is_this_for': 'Young defence aspirants dreaming of serving as commissioned officers in the Indian Army, Navy, or Air Force via NDA Khadakwasla.',
                    'eligibility': '10+2 appearing or passed (Age 16.5 to 19.5 years)',
                    'academic_level': 'UPSC NDA Syllabus (Maths + GAT)',
                    'exam_target': 'UPSC NDA & NA Exam I & II',
                    'pedagogy': [
                        'Maths Shortcut Techniques: Solving 120 questions in 150 minutes with speed formulas',
                        'Comprehensive GAT Mastery: High-scoring English and General Knowledge modules'
                    ]
                },
                'faqs': [
                    {'q': 'Does this program include SSB interview preparation?', 'a': 'Yes, the course includes SSB screening, OIR test practice, psychology tests overview, and personal interview tips.'}
                ],
                'subjects': [
                    {
                        'name': 'NDA Mathematics (300 Marks)',
                        'code': 'NDA-MATH',
                        'icon': 'shield',
                        'color_accent': '#15803D',
                        'teacher': t_math,
                        'chapters': [
                            ('Algebra & Matrices for NDA', 10.0, ['Sets, Relations & Functions', 'Complex Numbers & Quadratic Equations', 'Matrices & Determinants']),
                            ('Trigonometry & 2D/3D Geometry', 12.0, ['Trigonometric Equations & Properties of Triangles', 'Straight Lines & Conic Sections', '3D Coordinate Systems']),
                            ('Differential & Integral Calculus', 12.0, ['Limits, Continuity & Differentiation', 'Definite Integrals & Applications', 'Differential Equations'])
                        ]
                    },
                    {
                        'name': 'General Ability Test (GAT 600 Marks)',
                        'code': 'NDA-GAT',
                        'icon': 'compass',
                        'color_accent': '#991B1B',
                        'teacher': t_physics,
                        'chapters': [
                            ('English Grammar & Comprehension (200 Marks)', 10.0, ['Spotting Errors', 'Ordering of Words & Antonyms/Synonyms', 'Idioms & Sentence Completion']),
                            ('General Science (Physics, Chem, Bio - 200 Marks)', 12.0, ['General Physics Principles', 'Everyday Chemistry & Reactions', 'Basic Biology & Human Body']),
                            ('General Knowledge, History & Geography (200 Marks)', 10.0, ['Indian Freedom Struggle', 'World & Indian Geography', 'Current National & International Events'])
                        ]
                    }
                ]
            }
        ]

        # Seed courses and nested hierarchies
        for c_data in courses_data:
            course, created = Course.objects.update_or_create(
                slug=c_data['slug'],
                defaults={
                    'title': c_data['title'],
                    'category': c_data['category'],
                    'target_class': c_data['target_class'],
                    'duration_weeks': c_data['duration_weeks'],
                    'mode': c_data.get('mode', 'Offline Classroom & Live Hybrid'),
                    'badge_text': c_data.get('badge_text', ''),
                    'price': c_data['price'],
                    'discount_price': c_data.get('discount_price'),
                    'thumbnail_url': c_data['thumbnail_url'],
                    'short_description': c_data['short_description'],
                    'description': c_data['description'],
                    'features': c_data['features'],
                    'overview_data': c_data.get('overview_data', {}),
                    'faqs': c_data.get('faqs', []),
                    'is_featured': c_data.get('is_featured', False),
                    'order': c_data.get('order', 0),
                    'is_active': True
                }
            )
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} Course: {course.title}"))

            # Create default batches for this course
            batch_codes = [
                (f"{course.slug[:8].upper()}-MORNING", f"Morning Super-30 ({course.target_class})", "Mon, Wed, Fri (8:00 AM - 12:30 PM)", "Hall Alpha-1"),
                (f"{course.slug[:8].upper()}-EVENING", f"Evening Regular ({course.target_class})", "Tue, Thu, Sat (4:00 PM - 7:30 PM)", "Hall Beta-2"),
                (f"{course.slug[:8].upper()}-HYBRID", f"Weekend Hybrid Stream ({course.target_class})", "Saturday & Sunday (9:00 AM - 3:00 PM)", "Smart Digital Studio-A")
            ]

            for b_code, b_name, b_sched, b_room in batch_codes:
                batch, _ = Batch.objects.update_or_create(
                    code=b_code,
                    defaults={
                        'name': b_name,
                        'course': course,
                        'start_date': date.today() + timedelta(days=7),
                        'end_date': date.today() + timedelta(weeks=course.duration_weeks),
                        'schedule_time': b_sched,
                        'classroom': b_room,
                        'mode': 'HYBRID',
                        'max_capacity': 35
                    }
                )
                batch.teachers.add(default_teacher)

            # Create subjects and chapters
            for s_idx, s_data in enumerate(c_data.get('subjects', [])):
                subject, _ = Subject.objects.update_or_create(
                    course=course,
                    name=s_data['name'],
                    defaults={
                        'code': s_data.get('code', f"SUB-{s_idx+1}"),
                        'icon': s_data.get('icon', 'book-open'),
                        'color_accent': s_data.get('color_accent', '#3B82F6'),
                        'order': s_idx + 1,
                        'is_active': True
                    }
                )

                sub_teacher = s_data.get('teacher', default_teacher)

                for ch_idx, ch_info in enumerate(s_data.get('chapters', [])):
                    ch_title = ch_info[0]
                    ch_hours = ch_info[1]
                    ch_subtopics = ch_info[2] if len(ch_info) > 2 else []

                    chapter, _ = Chapter.objects.update_or_create(
                        subject=subject,
                        chapter_number=ch_idx + 1,
                        defaults={
                            'title': ch_title,
                            'estimated_hours': ch_hours,
                            'description': ' • '.join(ch_subtopics) if ch_subtopics else 'Comprehensive conceptual theory and practice questions.',
                            'order': ch_idx + 1,
                            'is_active': True
                        }
                    )

                    # Create Video Lesson for LMS and preview
                    VideoLesson.objects.get_or_create(
                        course=course,
                        subject=subject,
                        chapter=chapter,
                        order=1,
                        defaults={
                            'title': f"{ch_title} - Master Lecture 01",
                            'description': f"Fundamental principles, formulas, and live problem-solving on {ch_title}.",
                            'video_url': 'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ',
                            'thumbnail_url': course.thumbnail_url,
                            'duration_minutes': 50,
                            'is_published': True,
                            'is_free_preview': True if ch_idx == 0 else False,
                            'teacher': sub_teacher
                        }
                    )

                    # Create Study Material
                    StudyMaterial.objects.get_or_create(
                        course=course,
                        subject=subject,
                        chapter=chapter,
                        material_type='PDF_NOTES',
                        defaults={
                            'title': f"Handwritten Theory Notes & Formulas: {ch_title}",
                            'description': f"Comprehensive color-coded notes with solved examples for {ch_title}.",
                            'file_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
                            'file_size_mb': 3.2,
                            'teacher': sub_teacher,
                            'is_published': True
                        }
                    )

                    StudyMaterial.objects.get_or_create(
                        course=course,
                        subject=subject,
                        chapter=chapter,
                        material_type='DPP',
                        defaults={
                            'title': f"Daily Practice Problem (DPP Sheet #0{ch_idx+1}): {ch_title}",
                            'description': f"25 Graded questions with answer keys and hints.",
                            'file_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
                            'file_size_mb': 1.8,
                            'teacher': sub_teacher,
                            'is_published': True
                        }
                    )

        # Seed additional Toppers and Success Stories if needed
        toppers_data = [
            {'student_name': 'Aditya Singhania', 'exam_name': 'IIT-JEE Advanced 2025', 'rank_or_score': 'AIR 42', 'summary': 'IIT Bombay CSE • 2-Year Classroom Student', 'story': 'The structured test analysis and daily doubt support at Mayank Classes made all the difference.'},
            {'student_name': 'Dr. Shreya Mishra', 'exam_name': 'NEET-UG 2025', 'rank_or_score': '715 / 720 (AIR 18)', 'summary': 'AIIMS New Delhi • NEET Medical Champions Batch', 'story': 'NCERT line-by-line decoding in Biology and easy Physics shortcuts gave me the edge.'},
            {'student_name': 'Kavya Nair', 'exam_name': 'JEE Main 2025', 'rank_or_score': '99.94 Percentile (AIR 89)', 'summary': 'IIT Delhi EE • Pinnacle Batch', 'story': 'The computer-based test lab exactly simulated the actual NTA testing environment.'},
            {'student_name': 'Aryan Kulkarni', 'exam_name': 'Class 10 CBSE Boards & NTSE', 'rank_or_score': '99.2% & NTSE Scholar', 'summary': 'Foundation Batch Topper', 'story': 'Mayank Classes built my science and math foundation from Class 8 itself.'},
            {'student_name': 'Lt. Rohan Deshmukh', 'exam_name': 'UPSC NDA & NA 2025', 'rank_or_score': 'AIR 14 (NDA-153)', 'summary': 'National Defence Academy Khadakwasla', 'story': 'Rigorous mathematics speed drills and GAT classes prepared me perfectly.'}
        ]

        for top in toppers_data:
            SuccessStory.objects.update_or_create(
                student_name=top['student_name'],
                exam_name=top['exam_name'],
                defaults={
                    'rank_or_score': top['rank_or_score'],
                    'summary': top['summary'],
                    'story': top['story'],
                    'image_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500',
                    'year': 2025,
                    'is_featured': True
                }
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded comprehensive Mayank Classes Course Ecosystem!"))
