
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify as django_slugify
from utils.slug import generate_arabic_slug

def slugify(text):
    return generate_arabic_slug(text)
from accounts.models import Role
from college.models import College
from department.models import Department
from courses.models import Course, Unit, Lesson
from degreeLevel.models import DegreeLevel
from profiles.models import LecturerProfile, StudentProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with realistic Arabic demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting demo data generation...')
        
        # 1. Create Roles
        roles_data = [
            {'name': 'admin', 'description': 'مدير النظام'},
            {'name': 'staff', 'description': 'موظف'},
            {'name': 'lecturer', 'description': 'محاضر'},
            {'name': 'student', 'description': 'طالب'},
        ]
        
        for r in roles_data:
            Role.objects.get_or_create(name=r['name'], defaults={'description': r['description'], 'slug': slugify(r['name'])})
        self.stdout.write(self.style.SUCCESS('Roles created/verified.'))

        # 2. Create Colleges & Departments
        colleges_data = [
            {
                'title': 'كلية الهندسة وتكنولوجيا المعلومات',
                'description': 'كلية رائدة في مجالات الهندسة والتكنولوجيا والحوسبة.',
                'departments': [
                    {'name': 'هندسة البرمجيات', 'description': 'قسم يهتم بتطوير وصيانة الأنظمة البرمجية.'},
                    {'name': 'علوم الحاسوب', 'description': 'دراسة الخوارزميات وهياكل البيانات والأنظمة.'},
                    {'name': 'هندسة الشبكات', 'description': 'تصميم وإدارة شبكات الحاسوب والاتصالات.'},
                    {'name': 'الأمن السيبراني', 'description': 'حماية الأنظمة والبيانات من الهجمات الرقمية.'},
                ]
            },
            {
                'title': 'كلية العلوم الإدارية والمالية',
                'description': 'إعداد قادة المستقبل في مجال الإدارة والأعمال.',
                'departments': [
                    {'name': 'إدارة الأعمال', 'description': 'أساسيات إدارة المؤسسات والشركات.'},
                    {'name': 'المحاسبة', 'description': 'تسجيل وتلخيص المعاملات المالية.'},
                    {'name': 'التسويق الرقمي', 'description': 'استراتيجيات التسويق عبر المنصات الرقمية.'},
                ]
            },
            {
                'title': 'كلية التصاميم والفنون',
                'description': 'تنمية المهارات الإبداعية والفنية للطلاب.',
                'departments': [
                    {'name': 'التصميم الجرافيكي', 'description': 'فن الاتصال البصري باستخدام النصوص والصور.'},
                    {'name': 'التصميم الداخلي', 'description': 'تصميم المساحات الداخلية بشكل جمالي ووظيفي.'},
                ]
            }
        ]

        # 3. Create Lecturers (Users)
        lecturers_data = [
            {'email': 'ahmed@university.edu', 'first_name': 'أحمد', 'last_name': 'علي', 'password': 'password123'},
            {'email': 'sara@university.edu', 'first_name': 'سارة', 'last_name': 'محمد', 'password': 'password123'},
            {'email': 'khalid@university.edu', 'first_name': 'خالد', 'last_name': 'عبدالله', 'password': 'password123'},
            {'email': 'noor@university.edu', 'first_name': 'نور', 'last_name': 'يوسف', 'password': 'password123'},
            {'email': 'omar@university.edu', 'first_name': 'عمر', 'last_name': 'فاروق', 'password': 'password123'},
        ]

        created_lecturers = []
        for l_data in lecturers_data:
            user, created = User.objects.get_or_create(
                email=l_data['email'],
                defaults={
                    'first_name': l_data['first_name'],
                    'last_name': l_data['last_name'],
                    'profile_type': 'lecturer',
                    'is_staff': True
                }
            )
            if created:
                user.set_password(l_data['password'])
                user.save()
            created_lecturers.append(user)
        self.stdout.write(self.style.SUCCESS(f'{len(created_lecturers)} Lecturers available.'))


        # Create Colleges and Departments
        created_departments = []
        for c_data in colleges_data:
            # Generate slug manually to use in lookup
            c_slug = slugify(c_data['title'])
            college, created = College.objects.get_or_create(
                slug=c_slug,
                defaults={
                    'title': c_data['title'],
                    'description': c_data['description'], 
                    'is_public': True
                }
            )
            if not created and college.title != c_data['title']:
                college.title = c_data['title']
                college.save()
            
            for d_data in c_data['departments']:
                d_slug = slugify(d_data['name'])
                # Department slug must be unique globally according to the model (it's not unique_together with college in model definition I saw earlier, checking...)
                # The model says: slug = models.SlugField(unique=True...)
                
                # However, slugify might produce same slug for same department name in different colleges if names are identical. 
                # But here names are unique enough.
                
                dept, created = Department.objects.get_or_create(
                    slug=d_slug,
                    defaults={
                        'name': d_data['name'],
                        'college': college,
                        'description': d_data['description'], 
                        'is_active': True
                    }
                )
                if not created:
                    dept.name = d_data['name']
                    dept.college = college
                    dept.save()

                created_departments.append(dept)
        
        self.stdout.write(self.style.SUCCESS('Colleges and Departments created.'))

        # 4. Create Courses
        courses_data = [
            {
                'title': 'مقدمة في علوم الحاسوب',
                'dept_keyword': 'حاسوب',
                'description': '<p>هذا المساق يغطي أساسيات علوم الحاسوب بما في ذلك تاريخ الحوسبة، تمثيل البيانات، والبرمجة البسيطة.</p>',
                'units': [
                    {'title': 'أساسيات الحوسبة', 'lessons': ['تاريخ الحاسوب', 'مكونات الحاسوب المادية']},
                    {'title': 'تمثيل البيانات', 'lessons': ['النظام الثنائي', 'تحويلات الأنظمة العددية']},
                ]
            },
            {
                'title': 'برمجة بايثون للمبتدئين',
                'dept_keyword': 'برمجيات',
                'description': '<p>تعلم لغة بايثون من الصفر. المتغيرات، الجمل الشرطية، الحلقات، والدوال.</p>',
                'units': [
                    {'title': 'مقدمة في بايثون', 'lessons': ['تثبيت بايثون', 'كتابة أول برنامج']},
                    {'title': 'الهياكل الأساسية', 'lessons': ['المتغيرات وأنواع البيانات', 'الجمل الشرطية if-else']},
                ]
            },
            {
                'title': 'مبادئ التسويق الحديث',
                'dept_keyword': 'تسويق',
                'description': '<p>فهم المزيج التسويقي وسلوك المستهلك في العصر الرقمي.</p>',
                'units': [
                    {'title': 'مفاهيم التسويق', 'lessons': ['ما هو التسويق؟', 'تطور المفهوم التسويقي']},
                    {'title': 'البيئة التسويقية', 'lessons': ['تحليل البيئة الدقيقة', 'تحليل البيئة الكلية']},
                ]
            },
            {
                'title': 'أساسيات التصميم الجرافيكي',
                'dept_keyword': 'جرافيك',
                'description': '<p>مدخل إلى عالم التصميم الجرافيكي، نظرية الألوان، ومبادئ التكوين.</p>',
                'units': [
                    {'title': 'نظرية الألوان', 'lessons': ['عجلة الألوان', 'سيكولوجية الألوان']},
                    {'title': 'الطباعة', 'lessons': ['أنواع الخطوط', 'استخدام الخطوط في التصميم']},
                ]
            },
            {
                'title': 'إدارة الموارد البشرية',
                'dept_keyword': 'أعمال',
                'description': '<p>استراتيجيات استقطاب وتعيين وتطوير الكفاءات البشرية في المؤسسات.</p>',
                'units': [
                    {'title': 'تخطيط الموارد', 'lessons': ['أهمية التخطيط', 'تحليل الوظائف']},
                    {'title': 'التوظيف', 'lessons': ['مصادر الاستقطاب', 'مقابلات العمل']},
                ]
            },
             {
                'title': 'أمن المعلومات والشبكات',
                'dept_keyword': 'سيبراني',
                'description': '<p>حماية المعلومات والشبكات من التهديدات والاختراقات الأمنية.</p>',
                'units': [
                     {'title': 'مبادئ الأمن', 'lessons': ['السرية والسلامة والتوافر', 'أنواع الهجمات']},
                    {'title': 'التشفير', 'lessons': ['أساسيات التشفير', 'التوقيع الرقمي']},
                ]
            },
        ]

        for course_info in courses_data:
            # Find relevant department
            dept = next((d for d in created_departments if course_info['dept_keyword'] in d.name), created_departments[0])
            lecturer = random.choice(created_lecturers)
            
            c_slug = slugify(course_info['title'])
            course, created = Course.objects.get_or_create(
                slug=c_slug,
                defaults={
                    'title': course_info['title'],
                    'department': dept,
                    'lecturer': lecturer,
                    'description': course_info['description'],
                    'short_description': course_info['description'][:100], # Simple truncation
                    'is_active': True,
                    'academic_hours': random.randint(30, 60),
                }
            )

            if created: # Only add content for new courses to avoid duplication on re-run
                for unit_data in course_info['units']:
                    unit, _ = Unit.objects.get_or_create(
                        course=course,
                        title=unit_data['title'],
                        defaults={'slug': slugify(unit_data['title'])}
                    )
                    
                    for i, lesson_title in enumerate(unit_data['lessons']):
                        Lesson.objects.get_or_create(
                            course=course,
                            unit=unit,
                            title=lesson_title,
                            defaults={
                                'lesson_type': 'article',
                                'content': f'<p>محتوى تعليمي تجريبي لدرس: {lesson_title}.</p><p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، لقد تم توليد هذا النص من مولد النص العربى.</p>',
                                'order': i+1,
                                'duration': random.randint(5, 20),
                                'slug': slugify(lesson_title)
                            }
                        )

        
        self.stdout.write(self.style.SUCCESS(f'{len(courses_data)} Courses created with content.'))

        # 5. Create specific users (Students) if needed, but roles are enough for now.
        # Let's add one demo student
        student_email = 'student@university.edu'
        student_user, created = User.objects.get_or_create(
            email=student_email,
            defaults={
                'first_name': 'طالب',
                'last_name': 'مجتهد',
                'profile_type': 'student'
            }
        )
        if created:
            student_user.set_password('password123')
            student_user.save()
            self.stdout.write(self.style.SUCCESS('Demo Student created (student@university.edu / password123)'))

        self.stdout.write(self.style.SUCCESS('Done! Demo data populated successfully.'))
