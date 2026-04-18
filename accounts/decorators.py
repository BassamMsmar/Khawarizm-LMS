from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

def role_required(role_slugs):
    if not isinstance(role_slugs, list):
        role_slugs = [role_slugs]

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or any(request.user.has_role(role_slug) for role_slug in role_slugs):
                return view_func(request, *args, **kwargs)
            # عرض قالب HTML جميل، مع رمز حالة 403
            return render(request, 'accounts/unauthorized.html', status=403)
        return _wrapped_view
    return decorator

student_required = role_required('student')
lecturer_required = role_required('lecturer')
admin_required = role_required('admin')
staff_required = role_required(['admin', 'lecturer'])
