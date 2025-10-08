from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.db.models import Q
from courses.models import Lesson, Unit
from MainDashboard.forms import LessonForm
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator


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
