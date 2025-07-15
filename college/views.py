from django.shortcuts import render

# Create your views here.
def createCollege(request):
    return render(request, 'createCollege.html')

def collegeList(request):
    return render(request, 'collegeList.html')

def collegeDetail(request):
    return render(request, 'collegeDetail.html')


def collegeUpdate(request):
    return render(request, 'collegeUpdate.html')


def collegeDelete(request):
    return render(request, 'collegeDelete.html')
