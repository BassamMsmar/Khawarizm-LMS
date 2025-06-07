from django.shortcuts import HttpResponse, redirect


def baseDashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.user.roles.first().name == 'student':
        return redirect('dashboard:student')
    elif request.user.roles.first().name == 'staff':
        return redirect('dashboard:staff')
    elif request.user.roles.first().name == 'admin':
        return redirect('admin/')
    