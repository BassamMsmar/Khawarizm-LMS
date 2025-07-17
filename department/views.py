from django.shortcuts import render

# Create your views here.
def departmentList(request):
    return render(request, 'departmentList.html')

def createDepartment(request):
    return render(request, 'createDepartment.html')

def departmentDetail(request):
    return render(request, 'departmentDetail.html')

def departmentUpdate(request):
    return render(request, 'departmentUpdate.html')

def departmentDelete(request):
    return render(request, 'departmentDelete.html')
