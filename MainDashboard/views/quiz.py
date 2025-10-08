from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from courses.models import Quiz, Question, Choice, Unit
from MainDashboard.forms import QuizForm, QuestionForm, ChoiceForm
from accounts.decorators import staff_required
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


@staff_required
def delete_choice(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    question_id = choice.question.id
    choice.delete()
    return redirect('choice_list', question_id=question_id)
