from django.shortcuts import render, redirect
from .models import AboutPage

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('accounts:login')
    
    # Get the active AboutPage
    about_page = AboutPage.objects.filter(is_active=True).first()
    
    context = {
        'about_page': about_page,
    }
    
    return render(request, 'index.html', context)
