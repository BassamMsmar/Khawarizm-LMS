from django.shortcuts import render
from .models import Course, Lesson, Quiz
from django.views.generic import ListView, DetailView

# Create your views here.



class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


# class CourseDetail(DetailView):
#     model = Course
#     template_name = 'course_detail.html'
#     context_object_name = 'course'


from django.views.generic import DetailView
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, Unit, Quiz

class CourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Get units related to the course
        units = Unit.objects.filter(course=course)

        # Get lessons for each unit
        unit_lessons = {
            unit: unit.lessons.all() for unit in units
        }

        # Get quizzes for each unit
        unit_quizzes = {
            unit: unit.quizzes.filter(is_active=True) for unit in units
        }

        # Get lecturer profile
        lecturer_user = course.lecturer  # Assuming `lecturer` is a User
        lecturer_profile = getattr(lecturer_user, "lecturer_profile", None)

        context["related_units"] = units
        context["unit_lessons"] = unit_lessons
        context["unit_quizzes"] = unit_quizzes
        context["lecturer_profile"] = lecturer_profile


        return context

    

# class Lesson_Detail(DetailView):
#     model = Lesson
#     template_name = 'lesson.html'
#     context_object_name = 'lesson'
#     slug_url_kwarg = 'lesson_slug'


from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Unit, Quiz, Question, Choice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from datetime import timedelta

def Lesson_Detail(request, course_slug, lesson_slug):
    current_lesson = get_object_or_404(Lesson, slug=lesson_slug)
    units = Unit.objects.filter(course=current_lesson.unit.course)

    unit_lessons = {
        unit: unit.lessons.filter(is_active=True) for unit in units
    }

    context = {
        'lesson': current_lesson,
        'units': units,
        'unit_lessons': unit_lessons,
        'course': current_lesson.unit.course,
    }

    return render(request, 'lesson.html', context)


# Quiz Views
@login_required
def quiz_detail(request, course_slug, quiz_slug):
    """Display quiz details and start button"""
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    
    # Check if user has already taken this quiz
    # You might want to create a QuizAttempt model to track this
    
    context = {
        'quiz': quiz,
        'course': course,
        'questions_count': quiz.questions.count(),
    }
    
    return render(request, 'quiz_detail.html', context)


@login_required
def take_quiz(request, course_slug, quiz_slug):
    """Handle quiz taking with questions and timer"""
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    questions = quiz.questions.all().prefetch_related('choices')
    
    if request.method == 'POST':
        # Handle quiz submission
        user_answers = {}
        correct_answers = 0
        total_questions = questions.count()
        
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                selected_choice_id = request.POST[answer_key]
                user_answers[question.id] = int(selected_choice_id)
                
                # Check if answer is correct
                correct_choice = question.choices.filter(is_correct=True).first()
                if correct_choice and correct_choice.id == int(selected_choice_id):
                    correct_answers += 1
        
        # Calculate score
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Store results in session for result page
        request.session['quiz_results'] = {
            'quiz_id': quiz.id,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'user_answers': user_answers,
        }
        
        return redirect('courses:quiz_result', course_slug=course_slug, quiz_slug=quiz_slug)
    
    context = {
        'quiz': quiz,
        'course': course,
        'questions': questions,
        'quiz_duration': quiz.duration,  # in minutes
    }
    
    return render(request, 'take_quiz.html', context)


@login_required
def quiz_result(request, course_slug, quiz_slug):
    """Display quiz results with correct answers"""
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    
    # Get results from session
    quiz_results = request.session.get('quiz_results', {})
    
    if not quiz_results or quiz_results.get('quiz_id') != quiz.id:
        # Redirect to quiz detail if no results found
        return redirect('courses:quiz_detail', course_slug=course_slug, quiz_slug=quiz_slug)
    
    # Get questions with user answers and correct answers
    questions = quiz.questions.all().prefetch_related('choices')
    question_results = []
    
    for question in questions:
        user_answer_id = quiz_results['user_answers'].get(question.id)
        user_choice = None
        correct_choice = question.choices.filter(is_correct=True).first()
        
        if user_answer_id:
            user_choice = question.choices.filter(id=user_answer_id).first()
        
        question_results.append({
            'question': question,
            'user_choice': user_choice,
            'correct_choice': correct_choice,
            'is_correct': user_choice == correct_choice if user_choice else False,
        })
    
    context = {
        'quiz': quiz,
        'course': course,
        'score': quiz_results['score'],
        'correct_answers': quiz_results['correct_answers'],
        'total_questions': quiz_results['total_questions'],
        'question_results': question_results,
    }
    
    # Clear results from session
    if 'quiz_results' in request.session:
        del request.session['quiz_results']
    
    return render(request, 'quiz_result.html', context)
