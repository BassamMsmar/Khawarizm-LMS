from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Unit
from courses.models import Course, Lesson, Unit, Quiz, Question, Choice
from college.models import College
from department.models import Department
from .forms import CourseForm, CollegeForm, DepartmentForm, StudentForm, LessonForm, UnitForm, QuizForm, QuestionForm, ChoiceForm
from accounts.decorators import staff_required, admin_required
from django.utils.decorators import method_decorator

@staff_required
def quiz_list(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    quizzes = Quiz.objects.filter(unit=unit)
    context = {
        'unit': unit,
        'quizzes': quizzes
    }
    return render(request, 'pages/quiz_list.html', context)

@method_decorator(staff_required, name='dispatch')
class QuizCreateView(View):
    def get(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        form = QuizForm()
        context = {
            'form': form,
            'unit': unit
        }
        return render(request, 'pages/quiz_form.html', context)

    def post(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.unit = unit
            quiz.course = unit.course
            quiz.save()
            return redirect('quiz_list', unit_id=unit.id)
        context = {
            'form': form,
            'unit': unit
        }
        return render(request, 'pages/quiz_form.html', context)

@method_decorator(staff_required, name='dispatch')
class QuizUpdateView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        form = QuizForm(instance=quiz)
        context = {
            'form': form,
            'quiz': quiz
        }
        return render(request, 'pages/quiz_form.html', context)

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        form = QuizForm(request.POST, request.FILES, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list', unit_id=quiz.unit.id)
        context = {
            'form': form,
            'quiz': quiz
        }
        return render(request, 'pages/quiz_form.html', context)

@staff_required
def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    unit_id = quiz.unit.id
    quiz.delete()
    return redirect('quiz_list', unit_id=unit_id)

@staff_required
def lesson_list(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    lessons = Lesson.objects.filter(unit=unit)
    context = {
        'unit': unit,
        'lessons': lessons
    }
    return render(request, 'pages/lesson_list.html', context)

@method_decorator(staff_required, name='dispatch')
class LessonCreateView(View):
    def get(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        form = LessonForm()
        context = {
            'form': form,
            'unit': unit
        }
        return render(request, 'pages/lesson_form.html', context)

    def post(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.unit = unit
            lesson.course = unit.course
            lesson.save()
            return redirect('lesson_list', unit_id=unit.id)
        context = {
            'form': form,
            'unit': unit
        }
        return render(request, 'pages/lesson_form.html', context)

@method_decorator(staff_required, name='dispatch')
class LessonUpdateView(View):
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(instance=lesson)
        context = {
            'form': form,
            'lesson': lesson
        }
        return render(request, 'pages/lesson_form.html', context)

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_list', unit_id=lesson.unit.id)
        context = {
            'form': form,
            'lesson': lesson
        }
        return render(request, 'pages/lesson_form.html', context)

@staff_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    unit_id = lesson.unit.id
    lesson.delete()
    return redirect('lesson_list', unit_id=unit_id)

@staff_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    unit_form = UnitForm()
    lesson_form = LessonForm()
    quiz_form = QuizForm()
    context = {
        'course': course,
        'unit_form': unit_form,
        'lesson_form': lesson_form,
        'quiz_form': quiz_form
    }
    return render(request, 'pages/course_detail.html', context)

@method_decorator(staff_required, name='dispatch')
class UnitCreateAjaxView(View):
    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.course = course
            last_unit = course.maindashboard_units.all().order_by('-order').first()
            if last_unit:
                unit.order = last_unit.order + 1
            else:
                unit.order = 1
            unit.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@method_decorator(staff_required, name='dispatch')
class UnitUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(instance=unit)
        return JsonResponse({
            'form': form.as_p()
        })

    def post(self, request, pk, *args, **kwargs):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(request.POST, request.FILES, instance=unit)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@staff_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    course_id = unit.course.id
    unit.delete()
    return redirect('course_detail', course_id=course_id)

@method_decorator(staff_required, name='dispatch')
class LessonCreateAjaxView(View):
    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@method_decorator(staff_required, name='dispatch')
class LessonUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(instance=lesson)
        return JsonResponse({
            'form': form.as_p()
        })

    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@staff_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('course_detail', course_id=course_id)


from django.contrib.auth import get_user_model
from accounts.models import User, Role # Assuming Role model is in accounts.models

User = get_user_model()

# ____________________________________________________________________
from django.shortcuts import render
from courses.models import Course, Lesson  # أو حسب اسم الموديلات عندك
from accounts.models import User  # حسب مكان تعريف User

@staff_required
def dashboard(request):
    courses_count = Course.objects.count()

    students_count = User.objects.filter(roles__name__iexact='student').count()
    lessons_count = Lesson.objects.count()

    context = {
        'courses_count': courses_count,
        'students_count': students_count,
        'certificates_count': 58  # يمكنك تغييره لاحقًا إذا كان ديناميكي
    }

    return render(request, 'pages/dashboard.html', context)


@method_decorator(staff_required, name='dispatch')
class CollegeListView(ListView):
    model = College
    template_name = 'pages/colleges.html'
    context_object_name = 'colleges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollegeForm()
        return context


@method_decorator(staff_required, name='dispatch')
class LessonListView(ListView):
    model = Lesson
    template_name = 'pages/lessons.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LessonForm()
        return context


@method_decorator(staff_required, name='dispatch')
class LessonCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class LessonUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(instance=lesson)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': lesson.title,
                'course': lesson.course.id if lesson.course else '',
                'unit': lesson.unit.id if lesson.unit else '',
                'description': lesson.description,
                'content': lesson.content,
                'video_url': lesson.video_url,
                'video_file': str(lesson.video_file) if lesson.video_file else '',
                'duration': lesson.duration,
                'lesson_type': lesson.lesson_type,
                'pdf_file': str(lesson.pdf_file) if lesson.pdf_file else '',
                'image': str(lesson.image) if lesson.image else '',
                'url': lesson.url,
                'order': lesson.order,
                'is_active': lesson.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.delete()
    return redirect('/main-dashboard/lessons/')


@staff_required
def lesson_search_ajax(request):
    search_query = request.GET.get('q', '')
    lessons = Lesson.objects.all()

    if search_query:
        lessons = lessons.filter(
            Q(title__icontains=search_query) |
            Q(course__title__icontains=search_query) |
            Q(unit__title__icontains=search_query)
        ).distinct()

    lesson_data = []
    for lesson in lessons:
        lesson_data.append({
            'id': lesson.id,
            'slug': lesson.slug,
            'title': lesson.title,
            'course': lesson.course.title if lesson.course else '',
            'unit': lesson.unit.title if lesson.unit else '',
            'lesson_type': lesson.lesson_type,
            'duration': lesson.duration,
            'order': lesson.order,
            'is_active': lesson.is_active,
            'created_at': lesson.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'lessons': lesson_data})


@method_decorator(staff_required, name='dispatch')
class CollegeCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CollegeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class CollegeUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(instance=college)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': college.title,
                'about': college.about,
                'max_students': college.max_students,
                'is_public': college.is_public,
                'regular_price': str(college.regular_price) if college.regular_price else None,
                'discounted_price': str(college.discounted_price) if college.discounted_price else None,
                'intro_video_url': college.intro_video_url,
                'description': college.description,
                'tags': college.tags,
                'targeted_audience': college.targeted_audience,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(request.POST, request.FILES, instance=college)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_college(request, pk):
    college = College.objects.get(pk=pk)
    college.delete()
    return redirect('/main-dashboard/college/')


@staff_required
def college_search_ajax(request):
    search_query = request.GET.get('q', '')
    colleges = College.objects.all()

    if search_query:
        colleges = colleges.filter(
            Q(title__icontains=search_query)
        ).distinct()

    college_data = []
    for college in colleges:
        college_data.append({
            'id': college.id,
            'slug': college.slug,
            'title': college.title,
            'is_public': college.is_public,
            'max_students': college.max_students,
            'regular_price': str(college.regular_price) if college.regular_price else None,
            'discounted_price': str(college.discounted_price) if college.discounted_price else None,
        })

    return JsonResponse({'colleges': college_data})


# ____________________________________________________________________


@method_decorator(staff_required, name='dispatch')
class DepartmentListView(ListView):
    model = Department
    template_name = 'pages/departments.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollegeForm()
        return context


@method_decorator(staff_required, name='dispatch')
class CollegeCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CollegeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class CollegeUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(instance=college)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': college.title,
                'about': college.about,
                'max_students': college.max_students,
                'is_public': college.is_public,
                'regular_price': str(college.regular_price) if college.regular_price else None,
                'discounted_price': str(college.discounted_price) if college.discounted_price else None,
                'intro_video_url': college.intro_video_url,
                'description': college.description,
                'tags': college.tags,
                'targeted_audience': college.targeted_audience,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(request.POST, request.FILES, instance=college)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_college(request, pk):
    college = College.objects.get(pk=pk)
    college.delete()
    return redirect('/main-dashboard/college/')


@staff_required
def college_search_ajax(request):
    search_query = request.GET.get('q', '')
    colleges = College.objects.all()

    if search_query:
        colleges = colleges.filter(
            Q(title__icontains=search_query)
        ).distinct()

    college_data = []
    for college in colleges:
        college_data.append({
            'id': college.id,
            'slug': college.slug,
            'title': college.title,
            'is_public': college.is_public,
            'max_students': college.max_students,
            'regular_price': str(college.regular_price) if college.regular_price else None,
            'discounted_price': str(college.discounted_price) if college.discounted_price else None,
        })

    return JsonResponse({'colleges': college_data})


# ____________________________________________________________________


@method_decorator(staff_required, name='dispatch')
class DepartmentListView(ListView):
    model = Department
    template_name = 'pages/departments.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepartmentForm() # Add DepartmentForm to context
        return context


@method_decorator(staff_required, name='dispatch')
class DepartmentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class DepartmentUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(instance=department)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'name': department.name,
                'college': department.college.id if department.college else '',
                'admin': department.admin.id if department.admin else '',
                'is_active': department.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('/main-dashboard/departments/')


@staff_required
def department_search_ajax(request):
    search_query = request.GET.get('q', '')
    departments = Department.objects.all()

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(college__title__icontains=search_query) |
            Q(admin__first_name__icontains=search_query) |
            Q(admin__last_name__icontains=search_query)
        ).distinct()

    department_data = []
    for department in departments:
        department_data.append({
            'id': department.id,
            'slug': department.slug,
            'name': department.name,
            'college': department.college.title if department.college else '',
            'admin': department.admin.get_full_name() if department.admin else '',
            'is_active': department.is_active,
            'created_at': department.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'departments': department_data})


# ____________________________________________________________________


@method_decorator(staff_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'pages/courses.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lecturers'] = get_user_model().objects.all()
        context['form'] = CourseForm()

        return context


@method_decorator(staff_required, name='dispatch')
class CourseCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class CourseUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=course)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': course.title,
                'lecturer': course.lecturer.id if course.lecturer else '',
                'department': course.department.id if course.department else '',
                # أو لو عايز تبعت الاسم كمان
                'department_name': str(course.department) if course.department else '',
                'academic_hours': course.academic_hours,
                'short_description': course.short_description,
                'description': course.description,
                'what_youll_learn': course.what_youll_learn,
                'who_this_course_is_for': course.who_this_course_is_for,
                'is_active': course.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_course(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    return redirect('/main-dashboard/courses/')


@staff_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    unit_form = UnitForm()
    lesson_form = LessonForm()
    quiz_form = QuizForm()
    context = {
        'course': course,
        'unit_form': unit_form,
        'lesson_form': lesson_form,
        'quiz_form': quiz_form
    }
    return render(request, 'pages/course_detail.html', context)

@staff_required
def course_search_ajax(request):
    search_query = request.GET.get('q', '')
    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(lecturer__first_name__icontains=search_query) |
            Q(lecturer__last_name__icontains=search_query)
        ).distinct()

    course_data = []
    for course in courses:
        course_data.append({
            'id': course.id,
            'slug': course.slug,
            'title': course.title,
            'lecturer_full_name': course.lecturer.get_full_name(),
            'enrolled_count': course.get_enrolled_count(),
            'is_active': course.is_active,
            'created_at': course.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'courses': course_data})

# ____________________________________________________________________


User = get_user_model()

import json

@admin_required
def teachers(request):
    teachers = User.objects.filter(roles__name__iexact='lecturer')
    teacher_data = []
    for teacher in teachers:
        department = teacher.department
        college = department.college if department else None

        teacher_data.append({
            'teacher': {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'email': teacher.email,
                'created_at': teacher.created_at.isoformat() if teacher.created_at else None
            },
            'department': {
                'name': department.name if department else None
            },
            'college': {
                'title': college.title if college else None
            }
        })

    return render(request, 'pages/teachers.html', {'teacher_data': json.dumps(teacher_data)})


@method_decorator(admin_required, name='dispatch')
class TeacherCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.save()
            # Assign 'lecturer' role
            try:
                teacher_role = Role.objects.get(name='lecturer')
                teacher.roles.add(teacher_role)
            except Role.DoesNotExist:
                # Handle case where 'lecturer' role does not exist
                pass
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(admin_required, name='dispatch')
class TeacherUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(instance=teacher)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'email': teacher.email,
                'phone_number': teacher.phone_number,
                'department': teacher.department.id if teacher.department else ''
            }
        })

    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                teacher.set_password(password)
            teacher.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@admin_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    teacher.delete()
    return redirect('teachers')








# ____________________________________________________________________


User = get_user_model()

import json

@staff_required
def students(request):
    students = User.objects.filter(roles__name__iexact='student')
    student_data = []
    for student in students:
        department = student.department
        college = department.college if department else None

        student_data.append({
            'student': {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'is_active': student.is_active,
                'created_at': student.created_at.isoformat() if student.created_at else None
            },
            'department': {
                'name': department.name if department else None
            },
            'college': {
                'title': college.title if college else None
            }
        })

    return render(request, 'pages/students.html', {'student_data': json.dumps(student_data)})


@admin_required
def toggle_student_status(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.is_active = not student.is_active
    student.save()
    return JsonResponse({'success': True, 'is_active': student.is_active})


@method_decorator(admin_required, name='dispatch')
class StudentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            # Assign 'student' role
            try:
                student_role = Role.objects.get(name='student')
                student.roles.add(student_role)
            except Role.DoesNotExist:
                # Handle case where 'student' role does not exist
                pass
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

from .forms import UpdateStudentForm
@method_decorator(admin_required, name='dispatch')
class StudentUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(instance=student)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'phone_number': student.phone_number,
                'department': student.department.id if student.department else ''
            }
        })

    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                student.set_password(password)
            student.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@admin_required
def delete_student(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.delete()
    return redirect('students')

# ____________________________________________________________________


@staff_required
def lessons(request):
    return render(request, 'pages/lessons.html')


# ____________________________________________________________________

@staff_required
def quizzes(request):
    return render(request, 'pages/quizzes.html')


# ____________________________________________________________________


@staff_required
def reports(request):
    return render(request, 'pages/reports.html')


# ____________________________________________________________________


@staff_required
def settings(request):
    return render(request, 'pages/settings.html')

# ____________________________________________________________________

@staff_required
def question_list(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'pages/question_list.html', context)

@method_decorator(staff_required, name='dispatch')
class QuestionCreateView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        form = QuestionForm()
        context = {
            'form': form,
            'quiz': quiz
        }
        return render(request, 'pages/question_form.html', context)

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('question_list', quiz_id=quiz.id)
        context = {
            'form': form,
            'quiz': quiz
        }
        return render(request, 'pages/question_form.html', context)

@method_decorator(staff_required, name='dispatch')
class QuestionUpdateView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(instance=question)
        context = {
            'form': form,
            'question': question
        }
        return render(request, 'pages/question_form.html', context)

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list', quiz_id=question.quiz.id)
        context = {
            'form': form,
            'question': question
        }
        return render(request, 'pages/question_form.html', context)

@staff_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz_id = question.quiz.id
    question.delete()
    return redirect('question_list', quiz_id=quiz_id)

@staff_required
def choice_list(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    context = {
        'question': question,
        'choices': choices
    }
    return render(request, 'pages/choice_list.html', context)

@method_decorator(staff_required, name='dispatch')
class ChoiceCreateView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = ChoiceForm()
        context = {
            'form': form,
            'question': question
        }
        return render(request, 'pages/choice_form.html', context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('choice_list', question_id=question.id)
        context = {
            'form': form,
            'question': question
        }
        return render(request, 'pages/choice_form.html', context)

@method_decorator(staff_required, name='dispatch')
class ChoiceUpdateView(View):
    def get(self, request, pk):
        choice = get_object_or_404(Choice, pk=pk)
        form = ChoiceForm(instance=choice)
        context = {
            'form': form,
            'choice': choice
        }
        return render(request, 'pages/choice_form.html', context)

    def post(self, request, pk):
        choice = get_object_or_404(Choice, pk=pk)
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('choice_list', question_id=choice.question.id)
        context = {
            'form': form,
            'choice': choice
        }
        return render(request, 'pages/choice_form.html', context)

from student.models import Payment
from django.contrib.auth.decorators import login_required, permission_required

@staff_required
def payment_requests(request):
    pending_payments = Payment.objects.filter(status='pending').order_by('-created_at')
    other_payments = Payment.objects.exclude(status='pending').order_by('-created_at')
    context = {
        'pending_payments': pending_payments,
        'other_payments': other_payments,
    }
    return render(request, 'pages/payment_requests.html', context)

@staff_required
def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'approved'
    payment.save()
    return redirect('payment_requests')

@staff_required
def reject_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')
        if reason:
            payment.status = 'rejected'
            payment.rejection_reason = reason
            payment.save()
            return redirect('payment_requests')

    context = {
        'payment': payment,
    }
    return render(request, 'pages/reject_payment.html', context)
