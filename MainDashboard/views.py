from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'pages/dashboard.html')



def courses(request):
    return render(request, 'pages/courses.html')


def lessons(request):
    return render(request, 'pages/lessons.html')


def quizzes(request):
    return render(request, 'pages/quizzes.html')

def students(request):
    return render(request, 'pages/students.html')


def reports(request):
    return render(request, 'pages/reports.html')


def settings(request):
    return render(request, 'pages/settings.html')