from django.shortcuts import render

def blog(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/blog.html",data)

def blogDetails(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/blogDetails.html",data)

def blogGridMinimal(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/blogGridMinimal.html",data)

def blogList(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/blogList.html",data)

def blogWithSidebar(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/blogWithSidebar.html",data)

def postFormatAudio(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/postFormatAudio.html",data)

def postFormatGallery(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/postFormatGallery.html",data)

def postFormatQuote(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/postFormatQuote.html",data)

def postFormatStandard(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/postFormatStandard.html",data)

def postFormatVideo(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'rbt-header-sticky',
    }
    return render(request,"blog/postFormatVideo.html",data)
