from django.shortcuts import render

def artDesignSchool(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/artDesignSchool.html",data)

def checkout(request):
    data = {
        'topToBottom':'true',
        'footer':'false',
        'bodyClass':'rbt-header-sticky',

    }
    return render(request,"home/checkout.html",data)

def classicLms(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"home/classicLms.html",data)

def coaching(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/coaching.html",data)

def courseSchool(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/courseSchool.html",data)

def gymCoaching(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"home/gymCoaching.html",data)

def healthWellnessInstitute(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/healthWellnessInstitute.html",data)

def homeElegant(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/homeElegant.html",data)

def homeTechnology(request):
    data = {
        'header':'false',
        'footer':'false',
        'topToBottom':'true',
    }
    return render(request,"home/homeTechnology.html",data)

def instructorCourse(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'true',
    }
    return render(request,"home/instructorCourse.html",data)

def instructorPortfolio(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/instructorPortfolio.html",data)

def instructorsCoaches(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/instructorsCoaches.html",data)

def islamicCenter(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/islamicCenter.html",data)

def kindergarten(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky rbt-dark-header-8',
    }
    return render(request,"home/kindergarten.html",data)

def languageAcademy(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"home/languageAcademy.html",data)

def lifeCoach(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/lifeCoach.html",data)

def mainDemo(request):
    data = {
        'topToBottom':'true',
    }
    return render(request,"home/mainDemo.html",data)

def marketplace(request):
    data = {
        'header':'false',
        'footer':'false',
        'topToBottom':'true',
    }
    return render(request,"home/marketplace.html",data)

def modernUniversity(request):
    data = {
        'header':'false',
        'topToBottom':'true',
    }
    return render(request,"home/modernUniversity.html",data)

def multilingual(request):
    data = {
        'header':'false',
        'footer':'false',
        'topToBottom':'true',
    }
    return render(request,"home/multilingual.html",data)

def onlineAcademy(request):
    data = {
        'header':'false',
        'footer':'false',
        'topToBottom':'true',
    }
    return render(request,"home/onlineAcademy.html",data)

def onlineCourse(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/onlineCourse.html",data)

def onlineSchool(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"home/onlineSchool.html",data)

def singleCourse(request):
    data = {
        'header':'false',
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/singleCourse.html",data)

def udemyAffiliate(request):
    data = {
        'topToBottom':'true',
        'footer':'false',
    }
    return render(request,"home/udemyAffiliate.html",data)

def universityClassic(request):
    data = {
        'header':'false',
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"home/universityClassic.html",data)

def universityStatus(request):
    data = {
        'header':'false',
        'footer':'false',
        'topToBottom':'true',
    }
    return render(request,"home/universityStatus.html",data)

def wishlist(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"home/wishlist.html",data)
