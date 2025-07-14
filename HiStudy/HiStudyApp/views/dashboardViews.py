from django.shortcuts import render

def instructorAnnouncements(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorAnnouncements.html",data)

def instructorAssignments(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"dashboard/instructorDashboard/instructorAssignments.html",data)

def instructorDashboard(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorDashboard.html",data)

def instructorEnrolledCourses(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorEnrolledCourses.html",data)

def instructorMyQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"dashboard/instructorDashboard/instructorMyQuizAttempts.html",data)

def instructorOrderHistory(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorOrderHistory.html",data)


def instructorProfile(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorProfile.html",data)

def instructorQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorQuizAttempts.html",data)

def instructorReviews(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorReviews.html",data)

def instructorSettings(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorSettings.html",data)

def instructorWishlist(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/instructorDashboard/instructorWishlist.html",data)
    
def studentDashboard(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentDashboard.html",data)
    
def studentEnrolledCourses(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentEnrolledCourses.html",data)
    
def studentMyQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentMyQuizAttempts.html",data)
    
def studentOrderHistory(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentOrderHistory.html",data)
    
def studentProfile(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentProfile.html",data)
    
def studentReviews(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentReviews.html",data)
    
def studentSettings(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentSettings.html",data)
    
def studentWishlist(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentWishlist.html",data)
    