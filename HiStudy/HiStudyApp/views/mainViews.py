from django.shortcuts import render

def allQuestions(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"allQuestions.html",data)

def elements(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"elements.html",data)

def headerLayout(request):
    data = {
        'footer':'true',
        'bodyClass':'',
    }
    return render(request,"headerLayout.html",data)

def lessonAssignments(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"lessonAssignments.html",data)

def lessonAssignmentsSubmit(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"lessonAssignmentsSubmit.html",data)

def lessonIntro(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"lessonIntro.html",data)

def lessonQuiz(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"lessonQuiz.html",data)

def lessonQuizResult(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"lessonQuizResult.html",data)

def modal(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"modal.html",data)

def paginationQuiz(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"paginationQuiz.html",data)

def purchaseGuide(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"purchaseGuide.html",data)

def questionsTypes(request):
    data = {
        'header':'false',
        'topToBottom':'true',
    }
    return render(request,"questionsTypes.html",data)

def quizWithCustomTimer(request):
    data = {
        'header':'false',
        'topToBottom':'true',
    }
    return render(request,"quizWithCustomTimer.html",data)

def quizWithPoint(request):
    data = {
        'header':'false',
        'topToBottom':'true',
    }
    return render(request,"quizWithPoint.html",data)

def samplePageOne(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"samplePageOne.html",data)

def samplePageTwo(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"samplePageTwo.html",data)

def singleQuestion(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"singleQuestion.html",data)
