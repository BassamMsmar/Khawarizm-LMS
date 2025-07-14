from django.shortcuts import render


def aboutus01(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/aboutus01.html",data)

def aboutus02(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
        'footer':'false',
    }
    return render(request,"pages/aboutus02.html",data)

def academyGallery(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/academyGallery.html",data)

def admissionGuide(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/admissionGuide.html",data)

def becomeTeacher(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/becomeTeacher.html",data)

def cart(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/cart.html",data)

def contact(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/contact.html",data)

def eventDetails(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"pages/eventDetails.html",data)

def eventGrid(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/eventGrid.html",data)

def eventList(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/eventList.html",data)

def eventSidebar(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/eventSidebar.html",data)

def faqs(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/faqs.html",data)

def instructor(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/instructor.html",data)

def login(request):
    data = {
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
        'footer':'false',
    }
    return render(request,"pages/login.html",data)

def maintenance(request):
    data = {
        'bodyClass':'true',
        'switcher':'false',
        'header':'false',
        'footer':'false',
    }
    return render(request,"pages/maintenance.html",data)

def myAccount(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/myAccount.html",data)

def pageError(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/pageError.html",data)

def privacyPolicy(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"pages/privacyPolicy.html",data)

def profile(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',

    }
    return render(request,"pages/profile.html",data)

def shop(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/shop.html",data)

def singleProduct(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',

    }
    return render(request,"pages/singleProduct.html",data)

def subscription(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"pages/subscription.html",data)

def wishlist2(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"pages/wishlist2.html",data)


