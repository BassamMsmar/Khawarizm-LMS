from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Quiz, Unit, Question, Choice, Review
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Avg
from .forms import ReviewForm, QuizForm, QuestionForm, ChoiceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

class CourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        units = Unit.objects.filter(course=course)
        unit_lessons = {
            unit: unit.lessons.all() for unit in units
        }
        unit_quizzes = {
            unit: unit.quizzes.filter(is_active=True) for unit in units
        }

        completed_lessons = set()
        if self.request.user.is_authenticated:
            completed_lessons = set(self.request.user.completed_lessons.values_list('id', flat=True))

        context['completed_lessons'] = completed_lessons

        lecturer_user = course.lecturer
        lecturer_profile = getattr(lecturer_user, "lecturer_profile", None)

        context["related_units"] = units
        context["unit_lessons"] = unit_lessons
        context["unit_quizzes"] = unit_quizzes
        context["lecturer_profile"] = lecturer_profile

        reviews = course.reviews.all().order_by('-created_at')
        context['reviews'] = reviews
        context['review_count'] = reviews.count()

        average_rating = course.reviews.aggregate(Avg('rate'))['rate__avg']
        context['average_rating'] = round(average_rating, 1) if average_rating else 0

        rating_distribution = {
            5: course.reviews.filter(rate=5).count(),
            4: course.reviews.filter(rate=4).count(),
            3: course.reviews.filter(rate=3).count(),
            2: course.reviews.filter(rate=2).count(),
            1: course.reviews.filter(rate=1).count(),
        }
        context['rating_distribution'] = rating_distribution

        if context['review_count'] > 0:
            rating_percentages = {k: (v / context['review_count']) * 100 for k, v in rating_distribution.items()}
        else:
            rating_percentages = {k: 0 for k in rating_distribution.keys()}
        
        rating_progress = []
        for i in range(5, 0, -1):
            count = rating_distribution.get(i, 0)
            percentage = rating_percentages.get(i, 0)
            rating_progress.append((i, count, percentage))
            
        context['rating_progress'] = rating_progress

        context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.course = self.object
            review.user = request.user
            review.save()
            return redirect(self.get_success_url())
        else:
            print(form.errors)
            context = self.get_context_data(object=self.object)
            context['review_form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.get_object().slug})

def Lesson_Detail(request, course_slug, lesson_slug):
    current_lesson = get_object_or_404(Lesson, slug=lesson_slug)
    units = Unit.objects.filter(course=current_lesson.unit.course)

    unit_lessons = {
        unit: unit.lessons.filter(is_active=True) for unit in units
    }

    unit_quizzes = {
        unit: unit.quizzes.filter(is_active=True) for unit in units
    }

    completed_lessons = set()
    if request.user.is_authenticated:
        completed_lessons = set(request.user.completed_lessons.values_list('id', flat=True))

    is_completed = current_lesson.id in completed_lessons

    context = {
        'lesson': current_lesson,
        'units': units,
        'unit_lessons': unit_lessons,
        'unit_quizzes': unit_quizzes,
        'course': current_lesson.unit.course,
        'is_completed': is_completed,
        'completed_lessons': completed_lessons,
    }

    return render(request, 'lesson.html', context)

@login_required
def quiz_detail(request, course_slug, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    
    context = {
        'quiz': quiz,
        'course': course,
        'questions_count': quiz.questions.count(),
    }
    
    return render(request, 'quiz_detail.html', context)

@login_required
def take_quiz(request, course_slug, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    questions = quiz.questions.all().prefetch_related('choices')
    
    if request.method == 'POST':
        user_answers = {}
        correct_answers = 0
        total_questions = questions.count()
        
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                selected_choice_id = request.POST[answer_key]
                user_answers[question.id] = int(selected_choice_id)
                
                correct_choice = question.choices.filter(is_correct=True).first()
                if correct_choice and correct_choice.id == int(selected_choice_id):
                    correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
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
        'quiz_duration': quiz.duration,
    }
    
    return render(request, 'take_quiz.html', context)

@login_required
def quiz_result(request, course_slug, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    course = get_object_or_404(Course, slug=course_slug)
    
    quiz_results = request.session.get('quiz_results', {})
    
    if not quiz_results or quiz_results.get('quiz_id') != quiz.id:
        return redirect('courses:quiz_detail', course_slug=course_slug, quiz_slug=quiz_slug)
    
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
    
    if 'quiz_results' in request.session:
        del request.session['quiz_results']
    
    return render(request, 'quiz_result.html', context)

# Quiz CRUD Views
class QuizListView(ListView):
    model = Quiz
    template_name = 'courses/quiz_list.html'
    context_object_name = 'quizzes'

class QuizDetailView( DetailView):
    model = Quiz
    template_name = 'courses/quiz_detail.html'
    context_object_name = 'quiz'

class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'courses/quiz_form.html'
    success_url = reverse_lazy('courses:quiz_list')

class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'courses/quiz_form.html'
    success_url = reverse_lazy('courses:quiz_list')

class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'courses/quiz_confirm_delete.html'
    success_url = reverse_lazy('courses:quiz_list')

# Question CRUD Views
class QuestionListView(ListView):
    model = Question
    template_name = 'courses/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])
        return Question.objects.filter(quiz=self.quiz)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.quiz
        return context

class QuestionDetailView( DetailView):
    model = Question
    template_name = 'courses/question_detail.html'
    context_object_name = 'question'

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'courses/question_form.html'

    def form_valid(self, form):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])
        form.instance.quiz = quiz
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:question_list', kwargs={'quiz_pk': self.kwargs['quiz_pk']})

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'courses/question_form.html'

    def get_success_url(self):
        return reverse_lazy('courses:question_list', kwargs={'quiz_pk': self.object.quiz.pk})

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'courses/question_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('courses:question_list', kwargs={'quiz_pk': self.object.quiz.pk})

# Choice CRUD Views
class ChoiceListView( ListView):
    model = Choice
    template_name = 'courses/choice_list.html'
    context_object_name = 'choices'

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        return Choice.objects.filter(question=self.question)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context

class ChoiceDetailView( DetailView):
    model = Choice
    template_name = 'courses/choice_detail.html'
    context_object_name = 'choice'

class ChoiceCreateView( CreateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'courses/choice_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        return context

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        form.instance.question = question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:choice_create', kwargs={'question_pk': self.kwargs['question_pk']})

class ChoiceUpdateView( UpdateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'courses/choice_form.html'

    def get_success_url(self):
        return reverse_lazy('courses:choice_list', kwargs={'question_pk': self.object.question.pk})

class ChoiceDeleteView( DeleteView):
    model = Choice
    template_name = 'courses/choice_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('courses:choice_list', kwargs={'question_pk': self.object.question.pk})

@login_required
def mark_lesson_as_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.completed_by.add(request.user)
    return redirect('courses:lesson_detail', course_slug=lesson.course.slug, lesson_slug=lesson.slug)
