from django.shortcuts import render, redirect

def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'index.html')


# dfdfdfaf dfddfaf fdagdgs  agdgaga agd
