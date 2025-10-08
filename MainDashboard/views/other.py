from django.shortcuts import render
from accounts.decorators import staff_required


@staff_required
def lessons(request):
    return render(request, 'pages/lessons.html')


@staff_required
def quizzes(request):
    return render(request, 'pages/quizzes.html')


@staff_required
def reports(request):
    return render(request, 'pages/reports.html')


@staff_required
def settings(request):
    return render(request, 'pages/settings.html')
