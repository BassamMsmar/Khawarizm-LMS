from django.shortcuts import render

# Create your views here.
def degreeLevelList(request):
    return render(request, 'degreeLevel/listDegreeLevel.html')
def createDegreeLevel(request):
    return render(request, 'degreeLevel/createDegreeLevel.html')
def updateDegreeLevel(request):
    return render(request, 'degreeLevel/updateDegreeLevel.html')
def deleteDegreeLevel(request):
    return render(request, 'degreeLevel/deleteDegreeLevel.html')