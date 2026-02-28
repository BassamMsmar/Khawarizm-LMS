# Khawarizm Learning Management System (LMS)

### 🌟 نبذة عن المشروع (عربي)

نظام خوارزم لإدارة التعلم (Khawarizm LMS) هو مشروع مفتوح المصدر يهدف إلى تمكين وتسهيل التعليم الإلكتروني للمؤسسات التعليمية. يوفر النظام أدوات متكاملة لإدارة الدورات، وتسجيل الطلاب، والمتابعة الأكاديمية، والتواصل الفعال إلى جانب لوحة تحكم شاملة. نحن نرحب بجميع المساهمين والمطورين –سواء كانوا مبتدئين أو محترفين– للانضمام إلينا في تطوير هذا النظام خطوة بخطوة لجعله منصة التعليم الإلكتروني الأفضل للجميع.

---

### 🌟 Project Overview (English)

Khawarizm Learning Management System (LMS) is an open-source project dedicated to empowering and facilitating e-learning for educational institutions. It provides comprehensive tools for course management, student enrollment, academic tracking, and seamless educational workflows. Built with Django, it features a responsive dashboard and scalable architecture. We welcome developers and contributors of all skill levels to join us in shaping the future of e-learning.

---

## Features

- User authentication and authorization (Students, Instructors, Admins)
- Course management and enrollment
- Student profiles and academic tracking
- Department and degree level management
- Real-time notifications
- Responsive dashboard
- Rich text editing with CKEditor 5
- REST API endpoints

## Prerequisites

- Python 3.8 or higher
- PostgreSQL (or SQLite for development)
- pip (Python package manager)
- Git (for version control)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Khawarizm-LMS
```

### 2. Create and Activate Virtual Environment

#### Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Linux/MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/khawarizm_lms
```

### 5. Set Up Database

#### For PostgreSQL:

1. Create a new PostgreSQL database
2. Update the `DATABASES` setting in `project/settings.py` if needed

#### For SQLite (Development):

No additional setup required. SQLite will be used by default.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the application.

## Project Structure

- `accounts/`: User authentication and management
- `courses/`: Course management functionality
- `dashboard/`: Main dashboard views
- `college/`: College-related models and views
- `department/`: Department management
- `student/`: Student-specific functionality
- `notifications/`: Real-time notifications
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `project/`: Main project configuration

## API Documentation

API documentation is available at `/swagger/` or `/redoc/` when the development server is running.

## Testing

To run tests:

```bash
python manage.py test
```

## Contributing

### 🤝 كيفية المساهمة في المشروع (How to Contribute)

نحن نقدر أي مساهمة سواء كانت برمجية، تحسين في واجهة المستخدم، إضافة ميزات جديدة، كتابة اختبارات (Tests)، أو حتى تحديث الوثائق وإصلاح الأخطاء الإملائية. اتبع الخطوات التالية لإرسال مساهمتك:

1. **قم بعمل Fork** للمستودع إلى حسابك الشخصي.
2. **أنشئ فرعاً جديداً (Branch)** للعمل على الميزة أو التعديل:
   ```bash
   git checkout -b feature/amazing-feature
   ```
   _(قم بتسمية الفرع باسم يعبر عن التعديل، مثلاً: `fix/login-bug` أو `docs/update-readme`)_
3. **أضف تعديلاتك (Commit)** مع كتابة رسالة توضح ما قمت به بوضوح:
   ```bash
   git commit -m "Add responsive navigation bar"
   ```
4. **ارفع التعديلات (Push)** إلى مستودعك (الـ Fork الخاص بك):
   ```bash
   git push origin feature/amazing-feature
   ```
5. **قم بإنشاء Pull Request** في المستودع الأصلي للمشروع واشرح التعديلات التي قمت بها ليقوم الفريق بمراجعتها ودمجها.

**ملاحظة:** إذا واجهت أي مشكلة أو كان لديك اقتراح، لا تتردد في فتح **Issue** في المستودع لمناقشتها!

### Guidelines

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the repository or contact the development team.
