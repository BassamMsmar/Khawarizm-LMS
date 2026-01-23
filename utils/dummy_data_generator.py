"""
Comprehensive Demo Data Generator for Khawarizm LMS
Generates realistic Arabic academic data with AI-generated images
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from accounts.models import Role
from college.models import College
from department.models import Department
from courses.models import Course, Unit, Lesson, Quiz, Question, Choice, Review, QuizAttempt, AnsweredQuestion
from profiles.models import Language, StudentProfile, LecturerProfile
from degreeLevel.models import DegreeLevel

User = get_user_model()

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_progress(message, color=Colors.OKGREEN):
    """Print colored progress message"""
    print(f"{color}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_step(message):
    """Print step message"""
    print(f"{Colors.OKCYAN}➤ {message}{Colors.ENDC}")

# ============================================================================
# ARABIC DATA GENERATORS
# ============================================================================

ARABIC_MALE_NAMES = [
    'محمد', 'أحمد', 'علي', 'حسن', 'حسين', 'عمر', 'خالد', 'يوسف', 'إبراهيم', 'عبدالله',
    'عبدالرحمن', 'سعيد', 'فيصل', 'طارق', 'ماجد', 'سلطان', 'عادل', 'كريم', 'رامي', 'وليد',
    'ياسر', 'نبيل', 'جمال', 'كمال', 'سامي', 'هاني', 'زياد', 'فهد', 'بدر', 'نواف'
]

ARABIC_FEMALE_NAMES = [
    'فاطمة', 'عائشة', 'خديجة', 'مريم', 'زينب', 'سارة', 'نور', 'هدى', 'ليلى', 'رنا',
    'دينا', 'منى', 'سلمى', 'ريم', 'لينا', 'هالة', 'نادية', 'سمية', 'أمل', 'رشا',
    'نهى', 'إيمان', 'سناء', 'وفاء', 'هيفاء', 'شيماء', 'دعاء', 'آية', 'ملك', 'جنى'
]

ARABIC_FAMILY_NAMES = [
    'العلي', 'الأحمد', 'المحمد', 'الحسن', 'الحسين', 'السعيد', 'الخطيب', 'النجار', 'الحداد', 'الصباغ',
    'العمري', 'الفاروق', 'الشريف', 'القاضي', 'الطويل', 'الكبير', 'الصغير', 'البصري', 'الدمشقي', 'البغدادي',
    'الموصلي', 'الحلبي', 'المصري', 'الشامي', 'العراقي', 'اليمني', 'الحجازي', 'النجدي', 'الخليلي', 'العثماني'
]

ARABIC_CITIES = [
    'الرياض', 'جدة', 'مكة المكرمة', 'المدينة المنورة', 'الدمام', 'الخبر', 'الطائف', 'تبوك', 'بريدة', 'أبها',
    'القاهرة', 'الإسكندرية', 'دمشق', 'حلب', 'بغداد', 'البصرة', 'عمان', 'بيروت', 'الدوحة', 'دبي'
]

COLLEGES_DATA = [
    {
        'title': 'كلية الهندسة',
        'about': 'كلية الهندسة هي إحدى الكليات الرائدة في مجال التعليم الهندسي، تقدم برامج أكاديمية متميزة في مختلف التخصصات الهندسية.',
        'description': 'تسعى كلية الهندسة إلى تخريج مهندسين مؤهلين قادرين على المنافسة في سوق العمل المحلي والعالمي من خلال برامج تعليمية متطورة ومعامل حديثة.',
        'tags': 'هندسة, تكنولوجيا, علوم تطبيقية',
        'targeted_audience': 'الطلاب الراغبين في دراسة التخصصات الهندسية والتقنية',
        'image_prompt': 'Modern engineering college building with glass facade, students walking, professional architecture, bright daylight'
    },
    {
        'title': 'كلية علوم الحاسوب',
        'about': 'كلية علوم الحاسوب متخصصة في تقديم برامج أكاديمية متقدمة في علوم الحاسب والذكاء الاصطناعي وأمن المعلومات.',
        'description': 'تهدف الكلية إلى إعداد كوادر متخصصة في مجالات علوم الحاسوب والتقنيات الحديثة لتلبية احتياجات سوق العمل المتزايدة.',
        'tags': 'حاسوب, برمجة, ذكاء اصطناعي, أمن معلومات',
        'targeted_audience': 'الطلاب المهتمين بعلوم الحاسوب والبرمجة والتقنيات الحديثة',
        'image_prompt': 'Computer science college with modern computer labs, students coding, high-tech environment, blue lighting'
    },
    {
        'title': 'كلية إدارة الأعمال',
        'about': 'كلية إدارة الأعمال تقدم برامج أكاديمية شاملة في مجالات الإدارة والتسويق والمحاسبة وريادة الأعمال.',
        'description': 'تركز الكلية على تطوير مهارات القيادة والإدارة لدى الطلاب وتزويدهم بالمعرفة اللازمة لإدارة الأعمال بكفاءة.',
        'tags': 'إدارة, أعمال, تسويق, محاسبة, ريادة أعمال',
        'targeted_audience': 'الطلاب الراغبين في دراسة إدارة الأعمال والتسويق والمحاسبة',
        'image_prompt': 'Business school building, professional students in business attire, modern campus, corporate atmosphere'
    }
]

DEPARTMENTS_DATA = [
    # Engineering College Departments
    {
        'name': 'هندسة البرمجيات',
        'college_index': 0,
        'description': 'قسم هندسة البرمجيات يركز على تطوير البرمجيات وإدارة المشاريع البرمجية باستخدام أحدث المنهجيات والتقنيات.',
        'subscription_fee': Decimal('5000.00'),
        'image_prompt': 'Software engineering department, students coding on computers, modern workspace, collaborative environment'
    },
    {
        'name': 'هندسة الشبكات',
        'college_index': 0,
        'description': 'قسم هندسة الشبكات متخصص في تصميم وإدارة الشبكات الحاسوبية والاتصالات.',
        'subscription_fee': Decimal('4800.00'),
        'image_prompt': 'Network engineering lab with servers, cables, networking equipment, technical environment'
    },
    {
        'name': 'الأمن السيبراني',
        'college_index': 0,
        'description': 'قسم الأمن السيبراني يهتم بحماية الأنظمة والشبكات من الهجمات الإلكترونية وتأمين المعلومات.',
        'subscription_fee': Decimal('5500.00'),
        'image_prompt': 'Cybersecurity lab with security monitoring screens, dark room with blue screens, professional setup'
    },
    # Computer Science College Departments
    {
        'name': 'علوم البيانات',
        'college_index': 1,
        'description': 'قسم علوم البيانات يركز على تحليل البيانات الضخمة واستخراج المعرفة منها باستخدام تقنيات التعلم الآلي.',
        'subscription_fee': Decimal('5200.00'),
        'image_prompt': 'Data science lab with data visualization screens, charts and graphs, modern analytics workspace'
    },
    {
        'name': 'الذكاء الاصطناعي',
        'college_index': 1,
        'description': 'قسم الذكاء الاصطناعي متخصص في تطوير أنظمة ذكية قادرة على التعلم والتفكير واتخاذ القرارات.',
        'subscription_fee': Decimal('6000.00'),
        'image_prompt': 'AI research lab with robots, neural network diagrams, futuristic technology, innovative environment'
    },
    {
        'name': 'نظم المعلومات',
        'college_index': 1,
        'description': 'قسم نظم المعلومات يهتم بتصميم وتطوير أنظمة المعلومات لدعم العمليات التجارية والإدارية.',
        'subscription_fee': Decimal('4500.00'),
        'image_prompt': 'Information systems classroom, database diagrams, business process flows, professional learning space'
    },
    # Business College Departments
    {
        'name': 'إدارة الأعمال',
        'college_index': 2,
        'description': 'قسم إدارة الأعمال يقدم برامج شاملة في الإدارة والقيادة وإدارة الموارد البشرية.',
        'subscription_fee': Decimal('4000.00'),
        'image_prompt': 'Business management classroom, students in discussion, presentation screens, professional setting'
    },
    {
        'name': 'التسويق الرقمي',
        'college_index': 2,
        'description': 'قسم التسويق الرقمي متخصص في استراتيجيات التسويق الإلكتروني ووسائل التواصل الاجتماعي.',
        'subscription_fee': Decimal('4200.00'),
        'image_prompt': 'Digital marketing classroom, social media analytics, creative workspace, modern marketing tools'
    },
    {
        'name': 'المحاسبة',
        'college_index': 2,
        'description': 'قسم المحاسبة يركز على المبادئ المحاسبية والتدقيق والتحليل المالي.',
        'subscription_fee': Decimal('3800.00'),
        'image_prompt': 'Accounting classroom, financial charts, calculators, professional business environment'
    }
]

COURSES_DATA = {
    'هندسة البرمجيات': [
        {
            'title': 'برمجة بايثون المتقدمة',
            'short_description': 'تعلم البرمجة المتقدمة بلغة بايثون وتطبيقاتها في مختلف المجالات',
            'academic_hours': 45,
            'what_youll_learn': '<ul><li>البرمجة الكائنية المتقدمة</li><li>التعامل مع قواعد البيانات</li><li>تطوير تطبيقات الويب</li><li>معالجة البيانات</li></ul>',
            'who_this_course_is_for': '<p>المبرمجين الذين لديهم معرفة أساسية ببايثون ويريدون تطوير مهاراتهم</p>',
            'image_prompt': 'Python programming course thumbnail, code on screen, python logo, professional educational design'
        },
        {
            'title': 'تصميم قواعد البيانات',
            'short_description': 'أساسيات ومتقدمات تصميم وإدارة قواعد البيانات العلائقية',
            'academic_hours': 40,
            'what_youll_learn': '<ul><li>نمذجة البيانات</li><li>لغة SQL</li><li>تحسين الأداء</li><li>الأمان والنسخ الاحتياطي</li></ul>',
            'who_this_course_is_for': '<p>مطوري البرمجيات ومحللي الأنظمة المهتمين بقواعد البيانات</p>',
            'image_prompt': 'Database design course, database schema diagrams, SQL code, professional tech education'
        },
        {
            'title': 'تطوير تطبيقات الويب',
            'short_description': 'تعلم تطوير تطبيقات الويب الحديثة باستخدام أحدث التقنيات',
            'academic_hours': 50,
            'what_youll_learn': '<ul><li>HTML, CSS, JavaScript</li><li>إطارات العمل الحديثة</li><li>التصميم المتجاوب</li><li>واجهات برمجة التطبيقات</li></ul>',
            'who_this_course_is_for': '<p>المطورين الراغبين في تعلم تطوير تطبيقات الويب الكاملة</p>',
            'image_prompt': 'Web development course, modern website interface, code editor, responsive design mockups'
        }
    ],
    'هندسة الشبكات': [
        {
            'title': 'أساسيات الشبكات',
            'short_description': 'مقدمة شاملة لأساسيات الشبكات الحاسوبية والبروتوكولات',
            'academic_hours': 35,
            'what_youll_learn': '<ul><li>نموذج OSI</li><li>بروتوكولات TCP/IP</li><li>التوجيه والتبديل</li><li>تكوين الشبكات</li></ul>',
            'who_this_course_is_for': '<p>المبتدئين في مجال الشبكات والراغبين في فهم أساسياتها</p>',
            'image_prompt': 'Network fundamentals course, network diagram, routers and switches, educational tech illustration'
        },
        {
            'title': 'أمن الشبكات',
            'short_description': 'تعلم كيفية تأمين الشبكات من التهديدات والهجمات الإلكترونية',
            'academic_hours': 42,
            'what_youll_learn': '<ul><li>جدران الحماية</li><li>أنظمة كشف التسلل</li><li>التشفير</li><li>الشبكات الافتراضية الخاصة</li></ul>',
            'who_this_course_is_for': '<p>مهندسي الشبكات والمهتمين بأمن المعلومات</p>',
            'image_prompt': 'Network security course, firewall diagram, security shield, encrypted data flow illustration'
        }
    ],
    'الأمن السيبراني': [
        {
            'title': 'اختبار الاختراق الأخلاقي',
            'short_description': 'تعلم تقنيات اختبار الاختراق الأخلاقي وتأمين الأنظمة',
            'academic_hours': 48,
            'what_youll_learn': '<ul><li>جمع المعلومات</li><li>فحص الثغرات</li><li>الاستغلال</li><li>كتابة التقارير</li></ul>',
            'who_this_course_is_for': '<p>المتخصصين في الأمن السيبراني والراغبين في أن يصبحوا مختبري اختراق</p>',
            'image_prompt': 'Ethical hacking course, terminal with code, security testing tools, cybersecurity theme'
        },
        {
            'title': 'التحليل الجنائي الرقمي',
            'short_description': 'أساسيات التحليل الجنائي الرقمي والتحقيق في الجرائم الإلكترونية',
            'academic_hours': 40,
            'what_youll_learn': '<ul><li>جمع الأدلة الرقمية</li><li>تحليل الأقراص</li><li>استعادة البيانات</li><li>كتابة تقارير التحقيق</li></ul>',
            'who_this_course_is_for': '<p>المحققين والمهتمين بالتحليل الجنائي الرقمي</p>',
            'image_prompt': 'Digital forensics course, computer analysis, data recovery, investigation theme'
        }
    ],
    'علوم البيانات': [
        {
            'title': 'تحليل البيانات باستخدام Python',
            'short_description': 'تعلم تحليل البيانات وتصورها باستخدام مكتبات Python',
            'academic_hours': 45,
            'what_youll_learn': '<ul><li>Pandas و NumPy</li><li>تصور البيانات</li><li>التحليل الإحصائي</li><li>معالجة البيانات</li></ul>',
            'who_this_course_is_for': '<p>محللي البيانات والمبرمجين المهتمين بعلوم البيانات</p>',
            'image_prompt': 'Data analysis course, charts and graphs, Python code, data visualization dashboard'
        },
        {
            'title': 'التعلم الآلي',
            'short_description': 'مقدمة شاملة لخوارزميات التعلم الآلي وتطبيقاتها',
            'academic_hours': 50,
            'what_youll_learn': '<ul><li>الانحدار والتصنيف</li><li>التجميع</li><li>الشبكات العصبية</li><li>تقييم النماذج</li></ul>',
            'who_this_course_is_for': '<p>علماء البيانات والمطورين الراغبين في تعلم التعلم الآلي</p>',
            'image_prompt': 'Machine learning course, neural network diagram, AI algorithms, data science illustration'
        }
    ],
    'الذكاء الاصطناعي': [
        {
            'title': 'التعلم العميق',
            'short_description': 'تعلم بناء وتدريب الشبكات العصبية العميقة',
            'academic_hours': 52,
            'what_youll_learn': '<ul><li>الشبكات العصبية التلافيفية</li><li>الشبكات المتكررة</li><li>معالجة اللغة الطبيعية</li><li>رؤية الحاسوب</li></ul>',
            'who_this_course_is_for': '<p>المتخصصين في الذكاء الاصطناعي والتعلم الآلي</p>',
            'image_prompt': 'Deep learning course, neural network layers, AI brain illustration, advanced technology theme'
        },
        {
            'title': 'معالجة اللغة الطبيعية',
            'short_description': 'تعلم كيفية جعل الحواسيب تفهم وتعالج اللغة البشرية',
            'academic_hours': 46,
            'what_youll_learn': '<ul><li>تحليل النصوص</li><li>نماذج اللغة</li><li>الترجمة الآلية</li><li>تحليل المشاعر</li></ul>',
            'who_this_course_is_for': '<p>مطوري الذكاء الاصطناعي المهتمين بمعالجة اللغات</p>',
            'image_prompt': 'NLP course, text analysis, language processing, AI understanding human language illustration'
        }
    ],
    'نظم المعلومات': [
        {
            'title': 'تحليل وتصميم النظم',
            'short_description': 'تعلم منهجيات تحليل وتصميم نظم المعلومات',
            'academic_hours': 38,
            'what_youll_learn': '<ul><li>جمع المتطلبات</li><li>نمذجة النظم</li><li>تصميم قواعد البيانات</li><li>اختبار النظم</li></ul>',
            'who_this_course_is_for': '<p>محللي النظم ومطوري البرمجيات</p>',
            'image_prompt': 'Systems analysis course, UML diagrams, system design flowcharts, professional IT education'
        },
        {
            'title': 'إدارة المشاريع التقنية',
            'short_description': 'أساسيات إدارة مشاريع تقنية المعلومات',
            'academic_hours': 35,
            'what_youll_learn': '<ul><li>تخطيط المشاريع</li><li>إدارة الفرق</li><li>إدارة المخاطر</li><li>ضمان الجودة</li></ul>',
            'who_this_course_is_for': '<p>مديري المشاريع والمطورين الراغبين في تطوير مهارات الإدارة</p>',
            'image_prompt': 'IT project management course, Gantt chart, team collaboration, project planning illustration'
        }
    ],
    'إدارة الأعمال': [
        {
            'title': 'مبادئ الإدارة',
            'short_description': 'أساسيات الإدارة والقيادة في المنظمات',
            'academic_hours': 32,
            'what_youll_learn': '<ul><li>التخطيط والتنظيم</li><li>القيادة والتحفيز</li><li>اتخاذ القرارات</li><li>الرقابة والتقييم</li></ul>',
            'who_this_course_is_for': '<p>المديرين الجدد والراغبين في تطوير مهارات الإدارة</p>',
            'image_prompt': 'Management principles course, business leadership, organizational chart, professional business education'
        },
        {
            'title': 'إدارة الموارد البشرية',
            'short_description': 'تعلم إدارة وتطوير الموارد البشرية في المنظمات',
            'academic_hours': 36,
            'what_youll_learn': '<ul><li>التوظيف والاختيار</li><li>التدريب والتطوير</li><li>تقييم الأداء</li><li>التعويضات والمزايا</li></ul>',
            'who_this_course_is_for': '<p>مديري الموارد البشرية والمهتمين بإدارة الأفراد</p>',
            'image_prompt': 'HR management course, recruitment process, employee development, professional HR education'
        },
        {
            'title': 'ريادة الأعمال',
            'short_description': 'تعلم كيفية بدء وإدارة مشروعك الخاص',
            'academic_hours': 40,
            'what_youll_learn': '<ul><li>تطوير الأفكار</li><li>خطط الأعمال</li><li>التمويل</li><li>التسويق والمبيعات</li></ul>',
            'who_this_course_is_for': '<p>رواد الأعمال والراغبين في بدء مشاريعهم الخاصة</p>',
            'image_prompt': 'Entrepreneurship course, startup concept, business plan, innovation and creativity theme'
        }
    ],
    'التسويق الرقمي': [
        {
            'title': 'التسويق عبر وسائل التواصل الاجتماعي',
            'short_description': 'استراتيجيات التسويق الفعال عبر منصات التواصل الاجتماعي',
            'academic_hours': 34,
            'what_youll_learn': '<ul><li>استراتيجيات المحتوى</li><li>الإعلانات المدفوعة</li><li>تحليل البيانات</li><li>بناء المجتمعات</li></ul>',
            'who_this_course_is_for': '<p>المسوقين الرقميين وأصحاب الأعمال</p>',
            'image_prompt': 'Social media marketing course, social media icons, engagement metrics, digital marketing theme'
        },
        {
            'title': 'تحسين محركات البحث SEO',
            'short_description': 'تعلم كيفية تحسين ظهور موقعك في نتائج محركات البحث',
            'academic_hours': 30,
            'what_youll_learn': '<ul><li>البحث عن الكلمات المفتاحية</li><li>تحسين المحتوى</li><li>بناء الروابط</li><li>التحليل والتقارير</li></ul>',
            'who_this_course_is_for': '<p>المسوقين الرقميين ومطوري المواقع</p>',
            'image_prompt': 'SEO course, search engine results, keyword research, website optimization illustration'
        },
        {
            'title': 'التسويق بالمحتوى',
            'short_description': 'إنشاء محتوى تسويقي جذاب وفعال',
            'academic_hours': 32,
            'what_youll_learn': '<ul><li>استراتيجية المحتوى</li><li>كتابة المحتوى</li><li>التصميم البصري</li><li>قياس الأداء</li></ul>',
            'who_this_course_is_for': '<p>المسوقين وكتاب المحتوى</p>',
            'image_prompt': 'Content marketing course, creative content creation, blogging, storytelling illustration'
        }
    ],
    'المحاسبة': [
        {
            'title': 'مبادئ المحاسبة المالية',
            'short_description': 'أساسيات المحاسبة المالية والقوائم المالية',
            'academic_hours': 38,
            'what_youll_learn': '<ul><li>المعادلة المحاسبية</li><li>القيد المزدوج</li><li>القوائم المالية</li><li>التحليل المالي</li></ul>',
            'who_this_course_is_for': '<p>المحاسبين الجدد والمهتمين بالمحاسبة المالية</p>',
            'image_prompt': 'Financial accounting course, balance sheet, financial statements, professional accounting education'
        },
        {
            'title': 'المحاسبة الإدارية',
            'short_description': 'استخدام المعلومات المحاسبية في اتخاذ القرارات الإدارية',
            'academic_hours': 36,
            'what_youll_learn': '<ul><li>تحليل التكاليف</li><li>الموازنات</li><li>تقييم الأداء</li><li>اتخاذ القرارات</li></ul>',
            'who_this_course_is_for': '<p>المحاسبين والمديرين الماليين</p>',
            'image_prompt': 'Managerial accounting course, cost analysis, budgeting charts, business decision making'
        },
        {
            'title': 'التدقيق والمراجعة',
            'short_description': 'أساسيات التدقيق الداخلي والخارجي',
            'academic_hours': 40,
            'what_youll_learn': '<ul><li>معايير التدقيق</li><li>تخطيط عملية التدقيق</li><li>جمع الأدلة</li><li>كتابة التقارير</li></ul>',
            'who_this_course_is_for': '<p>المدققين والمحاسبين المهتمين بالتدقيق</p>',
            'image_prompt': 'Auditing course, financial review, audit checklist, professional accounting standards'
        }
    ]
}

DEGREE_LEVELS = [
    {'name': 'بكالوريوس', 'description': 'درجة البكالوريوس - المرحلة الجامعية الأولى'},
    {'name': 'ماجستير', 'description': 'درجة الماجستير - الدراسات العليا'},
    {'name': 'دكتوراه', 'description': 'درجة الدكتوراه - أعلى درجة أكاديمية'},
    {'name': 'دبلوم', 'description': 'الدبلوم - برامج تدريبية متخصصة'}
]

LANGUAGES_DATA = [
    {'name': 'العربية', 'code': 'ar'},
    {'name': 'English', 'code': 'en'},
    {'name': 'Français', 'code': 'fr'}
]

# ============================================================================
# IMAGE GENERATION HELPER
# ============================================================================

def generate_image_placeholder(prompt, filename):
    """
    Generate a placeholder for image (in production, this would call an AI image API)
    For now, we'll create a simple colored placeholder
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a colored image
        colors = [
            (52, 152, 219),   # Blue
            (46, 204, 113),   # Green
            (155, 89, 182),   # Purple
            (241, 196, 15),   # Yellow
            (230, 126, 34),   # Orange
            (231, 76, 60),    # Red
        ]
        
        color = random.choice(colors)
        img = Image.new('RGB', (800, 600), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = "Demo Image"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((800 - text_width) // 2, (600 - text_height) // 2)
        draw.text(position, text, fill=(255, 255, 255))
        
        # Save to bytes
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return ContentFile(img_io.read(), name=filename)
    except Exception as e:
        print(f"{Colors.WARNING}Warning: Could not generate image placeholder: {e}{Colors.ENDC}")
        return None

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_arabic_name(gender='male'):
    """Generate random Arabic name"""
    if gender == 'male':
        first_name = random.choice(ARABIC_MALE_NAMES)
    else:
        first_name = random.choice(ARABIC_FEMALE_NAMES)
    
    last_name = random.choice(ARABIC_FAMILY_NAMES)
    return first_name, last_name

def generate_email(first_name, last_name, domain='khawarizm.edu'):
    """Generate email from Arabic name"""
    # Simple transliteration for email
    email_name = f"{first_name}.{last_name}".lower()
    # Remove Arabic characters and replace with random string for demo
    import hashlib
    hash_name = hashlib.md5(email_name.encode()).hexdigest()[:8]
    return f"user_{hash_name}@{domain}"

@transaction.atomic
def create_roles():
    """Create user roles"""
    print_step("Creating roles...")
    roles_created = 0
    
    for role_name, role_display in [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student')
    ]:
        role, created = Role.objects.get_or_create(
            name=role_name,
            defaults={'description': f'{role_display} role'}
        )
        if created:
            roles_created += 1
    
    print(f"  ✓ Created {roles_created} roles (Total: {Role.objects.count()})")
    return Role.objects.all()

@transaction.atomic
def create_languages():
    """Create languages"""
    print_step("Creating languages...")
    languages_created = 0
    
    for lang_data in LANGUAGES_DATA:
        lang, created = Language.objects.get_or_create(
            code=lang_data['code'],
            defaults={'name': lang_data['name']}
        )
        if created:
            languages_created += 1
    
    print(f"  ✓ Created {languages_created} languages (Total: {Language.objects.count()})")
    return Language.objects.all()

@transaction.atomic
def create_colleges():
    """Create colleges with images"""
    print_step("Creating colleges with images...")
    colleges = []
    
    for college_data in COLLEGES_DATA:
        college, created = College.objects.get_or_create(
            title=college_data['title'],
            defaults={
                'about': college_data['about'],
                'description': college_data['description'],
                'tags': college_data['tags'],
                'targeted_audience': college_data['targeted_audience'],
                'max_students': random.randint(500, 2000),
                'is_public': True,
                'regular_price': Decimal(str(random.randint(10000, 20000))),
                'discounted_price': Decimal(str(random.randint(8000, 15000)))
            }
        )
        
        if created:
            # Generate and attach image
            image = generate_image_placeholder(
                college_data['image_prompt'],
                f"college_{college.slug}.jpg"
            )
            if image:
                college.thumbnail = image
                college.save()
        
        colleges.append(college)
    
    print(f"  ✓ Created {len(colleges)} colleges")
    return colleges

@transaction.atomic
def create_departments(colleges):
    """Create departments with images"""
    print_step("Creating departments with images...")
    departments = []
    
    for dept_data in DEPARTMENTS_DATA:
        college = colleges[dept_data['college_index']]
        
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            college=college,
            defaults={
                'description': dept_data['description'],
                'subscription_fee': dept_data['subscription_fee']
            }
        )
        
        if created:
            # Generate and attach image
            image = generate_image_placeholder(
                dept_data['image_prompt'],
                f"dept_{dept.slug}.jpg"
            )
            if image:
                dept.image = image
                dept.thumbnail = image
                dept.save()
        
        departments.append(dept)
    
    print(f"  ✓ Created {len(departments)} departments")
    return departments

@transaction.atomic
def create_admin_users(roles):
    """Create admin users"""
    print_step("Creating admin users...")
    admin_role = Role.objects.get(name='admin')
    staff_role = Role.objects.get(name='staff')
    admins = []
    
    admin_data = [
        ('محمد', 'الأحمد', 'male'),
        ('فاطمة', 'العلي', 'female')
    ]
    
    for first_name, last_name, gender in admin_data:
        email = generate_email(first_name, last_name)
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'date_of_birth': datetime.now().date() - timedelta(days=random.randint(10000, 15000)),
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'profile_type': 'lecturer'
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            user.roles.add(admin_role, staff_role)
        
        admins.append(user)
    
    print(f"  ✓ Created {len(admins)} admin users")
    return admins

@transaction.atomic
def create_lecturers(departments, roles):
    """Create lecturer users with profiles"""
    print_step("Creating lecturers with profiles and images...")
    lecturer_role = Role.objects.get(name='lecturer')
    lecturers = []
    
    for i in range(15):
        gender = random.choice(['male', 'female'])
        first_name, last_name = generate_arabic_name(gender)
        email = generate_email(first_name, last_name)
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'date_of_birth': datetime.now().date() - timedelta(days=random.randint(10000, 18000)),
                'is_staff': False,
                'is_active': True,
                'profile_type': 'lecturer',
                'phone_number': f'+966{random.randint(500000000, 599999999)}'
            }
        )
        
        if created:
            user.set_password('lecturer123')
            user.save()
            user.roles.add(lecturer_role)
            
            # Assign department
            dept = random.choice(departments)
            user.department = dept
            user.save()
            
            # Create lecturer profile
            profile, _ = LecturerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'headline': f'محاضر متخصص في {dept.name}',
                    'bio': f'محاضر ذو خبرة واسعة في مجال {dept.name} مع سنوات من الخبرة الأكاديمية والعملية.',
                    'experience': random.randint(5, 20),
                    'education': 'دكتوراه في التخصص',
                    'certification': 'شهادات مهنية متعددة في المجال',
                    'city': random.choice(ARABIC_CITIES),
                    'country': 'SA'
                }
            )
            
            # Generate profile picture
            image = generate_image_placeholder(
                f"Professional {'male' if gender == 'male' else 'female'} lecturer portrait, academic setting",
                f"lecturer_{user.id}.jpg"
            )
            if image:
                profile.profile_picture = image
                profile.save()
            
            # Add languages
            profile.languages.add(*Language.objects.filter(code__in=['ar', 'en']))
            profile.departments.add(dept)
        
        lecturers.append(user)
    
    print(f"  ✓ Created {len(lecturers)} lecturers with profiles")
    return lecturers

@transaction.atomic
def create_students(departments, roles):
    """Create student users with profiles"""
    print_step("Creating students with profiles and images...")
    student_role = Role.objects.get(name='student')
    students = []
    
    for i in range(50):
        gender = random.choice(['male', 'female'])
        first_name, last_name = generate_arabic_name(gender)
        email = generate_email(first_name, last_name)
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'date_of_birth': datetime.now().date() - timedelta(days=random.randint(6500, 9000)),
                'is_staff': False,
                'is_active': True,
                'profile_type': 'student',
                'phone_number': f'+966{random.randint(500000000, 599999999)}'
            }
        )
        
        if created:
            user.set_password('student123')
            user.save()
            user.roles.add(student_role)
            
            # Assign department
            dept = random.choice(departments)
            user.department = dept
            user.save()
            
            # Create student profile
            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'طالب في قسم {dept.name}، متحمس للتعلم والتطوير.',
                    'college': dept.college,
                    'department': dept,
                    'city': random.choice(ARABIC_CITIES),
                    'country': 'SA',
                    'certificate_number': f'CERT-{random.randint(10000, 99999)}'
                }
            )
            
            # Generate profile picture
            image = generate_image_placeholder(
                f"Professional {'male' if gender == 'male' else 'female'} student portrait, young person",
                f"student_{user.id}.jpg"
            )
            if image:
                profile.profile_picture = image
                profile.save()
            
            # Add languages
            profile.languages.add(*Language.objects.filter(code__in=['ar', 'en']))
        
        students.append(user)
    
    print(f"  ✓ Created {len(students)} students with profiles")
    return students

@transaction.atomic
def create_degree_levels(departments):
    """Create degree levels"""
    print_step("Creating degree levels...")
    degree_levels = []
    
    for level_data in DEGREE_LEVELS:
        for dept in departments[:3]:  # Create for first 3 departments
            from django.utils.text import slugify
            
            # Pre-generate name and slug to ensure uniqueness
            name = f"{level_data['name']} - {dept.name}"
            slug = slugify(name)
            
            level, created = DegreeLevel.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'department': dept,
                    'description': level_data['description']
                }
            )
            
            if created:
                # Generate image
                image = generate_image_placeholder(
                    f"Academic degree certificate, {level_data['name']}, professional education",
                    f"degree_{level.slug}.jpg"
                )
                if image:
                    level.image = image
                    level.thumbnail = image
                    level.save()
            
            degree_levels.append(level)
    
    print(f"  ✓ Created {len(degree_levels)} degree levels")
    return degree_levels

@transaction.atomic
def create_courses(departments, lecturers):
    """Create courses with images"""
    print_step("Creating courses with images...")
    courses = []
    
    for dept in departments:
        dept_name = dept.name
        if dept_name in COURSES_DATA:
            for course_data in COURSES_DATA[dept_name]:
                # Assign random lecturer from same department
                dept_lecturers = [l for l in lecturers if l.department == dept]
                if not dept_lecturers:
                    dept_lecturers = lecturers[:3]  # Fallback
                
                lecturer = random.choice(dept_lecturers)
                
                course, created = Course.objects.get_or_create(
                    title=course_data['title'],
                    department=dept,
                    defaults={
                        'lecturer': lecturer,
                        'short_description': course_data['short_description'],
                        'academic_hours': course_data['academic_hours'],
                        'what_youll_learn': course_data['what_youll_learn'],
                        'who_this_course_is_for': course_data['who_this_course_is_for'],
                        'description': f"<p>{course_data['short_description']}</p>",
                        'is_active': True
                    }
                )
                
                if created:
                    # Generate course image
                    image = generate_image_placeholder(
                        course_data['image_prompt'],
                        f"course_{course.slug}.jpg"
                    )
                    if image:
                        course.image = image
                        course.thumbnail = image
                        course.save()
                    
                    # Add to lecturer profile
                    if hasattr(lecturer, 'lecturer_profile'):
                        lecturer.lecturer_profile.courses.add(course)
                
                courses.append(course)
    
    print(f"  ✓ Created {len(courses)} courses")
    return courses

@transaction.atomic
def create_course_content(courses):
    """Create units, lessons, and quizzes for courses"""
    print_step("Creating course content (units, lessons, quizzes)...")
    
    lesson_types = ['video', 'article', 'pdf']
    units_created = 0
    lessons_created = 0
    quizzes_created = 0
    
    for course in courses:
        # Create 3-5 units per course
        num_units = random.randint(3, 5)
        
        for unit_num in range(1, num_units + 1):
            unit, created = Unit.objects.get_or_create(
                title=f"الوحدة {unit_num}: {course.title}",
                course=course,
                defaults={}
            )
            
            if created:
                units_created += 1
                
                # Create 5-8 lessons per unit
                num_lessons = random.randint(5, 8)
                for lesson_num in range(1, num_lessons + 1):
                    lesson_type = random.choice(lesson_types)
                    
                    lesson, l_created = Lesson.objects.get_or_create(
                        title=f"الدرس {lesson_num}: محتوى الوحدة {unit_num}",
                        unit=unit,
                        course=course,
                        defaults={
                            'description': f"<p>شرح مفصل للدرس {lesson_num} من الوحدة {unit_num}</p>",
                            'content': f"<p>محتوى تعليمي شامل يغطي جميع جوانب الموضوع</p>",
                            'lesson_type': lesson_type,
                            'duration': random.randint(10, 60),
                            'order': lesson_num,
                            'is_active': True
                        }
                    )
                    
                    if l_created:
                        lessons_created += 1
                
                # Create 1-2 quizzes per unit
                num_quizzes = random.randint(1, 2)
                for quiz_num in range(1, num_quizzes + 1):
                    quiz, q_created = Quiz.objects.get_or_create(
                        title=f"اختبار الوحدة {unit_num} - الجزء {quiz_num}",
                        unit=unit,
                        defaults={
                            'duration': random.randint(20, 60),
                            'is_active': True
                        }
                    )
                    
                    if q_created:
                        quizzes_created += 1
                        
                        # Create 5-10 questions per quiz
                        num_questions = random.randint(5, 10)
                        for q_num in range(1, num_questions + 1):
                            question = Question.objects.create(
                                quiz=quiz,
                                text=f"السؤال {q_num}: ما هو المفهوم الأساسي المتعلق بهذا الموضوع؟"
                            )
                            
                            # Create 4 choices per question
                            for choice_num in range(1, 5):
                                Choice.objects.create(
                                    question=question,
                                    text=f"الخيار {choice_num}",
                                    is_correct=(choice_num == 1)  # First choice is correct
                                )
    
    print(f"  ✓ Created {units_created} units, {lessons_created} lessons, {quizzes_created} quizzes")

@transaction.atomic
def enroll_students_and_create_progress(courses, students):
    """Enroll students in courses and create progress data"""
    print_step("Enrolling students and creating progress data...")
    
    enrollments = 0
    completions = 0
    attempts = 0
    reviews = 0
    
    for student in students:
        # Each student enrolls in 2-5 courses
        num_courses = random.randint(2, 5)
        student_courses = random.sample(list(courses), min(num_courses, len(courses)))
        
        for course in student_courses:
            # Enroll student
            course.students_enrolled.add(student)
            enrollments += 1
            
            # Add course to student profile
            if hasattr(student, 'student_profile'):
                student.student_profile.course.add(course)
            
            # Complete some lessons (50-80% of lessons)
            lessons = list(course.lessons.all())
            if lessons:
                num_to_complete = int(len(lessons) * random.uniform(0.5, 0.8))
                completed_lessons = random.sample(lessons, num_to_complete)
                
                for lesson in completed_lessons:
                    lesson.completed_by.add(student)
                    completions += 1
            
            # Attempt some quizzes
            units = course.units.all()
            for unit in units:
                quizzes = unit.quizzes.all()
                for quiz in quizzes:
                    if random.random() > 0.3:  # 70% chance to attempt
                        score = random.uniform(60, 100)
                        attempt = QuizAttempt.objects.create(
                            user=student,
                            quiz=quiz,
                            score=score
                        )
                        attempts += 1
                        
                        # Create answered questions
                        for question in quiz.questions.all():
                            choices = list(question.choices.all())
                            if choices:
                                selected = random.choice(choices)
                                AnsweredQuestion.objects.create(
                                    quiz_attempt=attempt,
                                    question=question,
                                    selected_choice=selected,
                                    is_correct=selected.is_correct
                                )
            
            # Add review (30% chance)
            if random.random() > 0.7:
                Review.objects.create(
                    course=course,
                    user=student,
                    rate=random.randint(3, 5),
                    comment=random.choice([
                        'مقرر ممتاز واستفدت منه كثيراً',
                        'شرح واضح ومفيد جداً',
                        'محتوى قيم ومنظم بشكل جيد',
                        'تجربة تعليمية رائعة',
                        'أنصح بهذا المقرر بشدة'
                    ])
                )
                reviews += 1
    
    print(f"  ✓ Created {enrollments} enrollments, {completions} lesson completions")
    print(f"  ✓ Created {attempts} quiz attempts, {reviews} reviews")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print_progress("🚀 Starting Comprehensive Demo Data Generation", Colors.HEADER)
    print(f"{Colors.BOLD}Khawarizm LMS - Professional Demo Data System{Colors.ENDC}\n")
    
    start_time = datetime.now()
    
    try:
        # Step 1: Create roles
        print_progress("📋 Step 1: Creating Roles", Colors.OKBLUE)
        roles = create_roles()
        
        # Step 2: Create languages
        print_progress("🌍 Step 2: Creating Languages", Colors.OKBLUE)
        languages = create_languages()
        
        # Step 3: Create colleges
        print_progress("🏛️ Step 3: Creating Colleges", Colors.OKBLUE)
        colleges = create_colleges()
        
        # Step 4: Create departments
        print_progress("📚 Step 4: Creating Departments", Colors.OKBLUE)
        departments = create_departments(colleges)
        
        # Step 5: Create users
        print_progress("👥 Step 5: Creating Users", Colors.OKBLUE)
        admins = create_admin_users(roles)
        lecturers = create_lecturers(departments, roles)
        students = create_students(departments, roles)
        
        # Step 6: Create degree levels
        print_progress("🎓 Step 6: Creating Degree Levels", Colors.OKBLUE)
        degree_levels = create_degree_levels(departments)
        
        # Step 7: Create courses
        print_progress("📖 Step 7: Creating Courses", Colors.OKBLUE)
        courses = create_courses(departments, lecturers)
        
        # Step 8: Create course content
        print_progress("📝 Step 8: Creating Course Content", Colors.OKBLUE)
        create_course_content(courses)
        
        # Step 9: Enroll students and create progress
        print_progress("✅ Step 9: Creating Enrollments and Progress", Colors.OKBLUE)
        enroll_students_and_create_progress(courses, students)
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print_progress("✨ Demo Data Generation Complete!", Colors.OKGREEN)
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  • Roles: {Role.objects.count()}")
        print(f"  • Languages: {Language.objects.count()}")
        print(f"  • Colleges: {College.objects.count()}")
        print(f"  • Departments: {Department.objects.count()}")
        print(f"  • Users: {User.objects.count()}")
        print(f"    - Admins: {len(admins)}")
        print(f"    - Lecturers: {len(lecturers)}")
        print(f"    - Students: {len(students)}")
        print(f"  • Degree Levels: {DegreeLevel.objects.count()}")
        print(f"  • Courses: {Course.objects.count()}")
        print(f"  • Units: {Unit.objects.count()}")
        print(f"  • Lessons: {Lesson.objects.count()}")
        print(f"  • Quizzes: {Quiz.objects.count()}")
        print(f"  • Questions: {Question.objects.count()}")
        print(f"  • Quiz Attempts: {QuizAttempt.objects.count()}")
        print(f"  • Reviews: {Review.objects.count()}")
        print(f"\n{Colors.OKGREEN}⏱️  Total time: {duration:.2f} seconds{Colors.ENDC}\n")
        
        print(f"{Colors.WARNING}📌 Default Passwords:{Colors.ENDC}")
        print(f"  • Admins: admin123")
        print(f"  • Lecturers: lecturer123")
        print(f"  • Students: student123\n")
        
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Error during data generation: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
