from django.shortcuts import render


def courseCard2(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseCard2.html",data)

def courseCard3(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseCard3.html",data)

def courseDetails(request):
    data = {
        'footer':'false',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails.html",data)

def courseDetails2(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails2.html",data)

def courseDetails3(request):
    data = {
        'footer':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails3.html",data)

def courseFilterOneOpen(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseFilterOneOpen.html",data)

def courseFilterOneToggle(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseFilterOneToggle.html",data)

def courseFilterTwoOpen(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseFilterTwoOpen.html",data)

def courseFilterTwoToggle(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseFilterTwoToggle.html",data)

def courseMasonry(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseMasonry.html",data)

def courseWithSidebar(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseWithSidebar.html",data)

def courseWithTab(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseWithTab.html",data)

def courseWithTabTwo(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"courses/courseWithTabTwo.html",data)

def createCourse(request):
    data = {
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"courses/createCourse.html",data)

def instructorCourse(request):
    data = {
        'footer':'true',
        'bodyClass':'',
    }
    return render(request,"courses/instructorCourse.html",data)

def lesson(request):
    return render(request,"courses/lesson.html")
