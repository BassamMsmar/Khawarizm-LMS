from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(role_slugs):
    if not isinstance(role_slugs, list):
        role_slugs = [role_slugs]

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if not any(request.user.has_role(role_slug) for role_slug in role_slugs):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

student_required = role_required('student')
teacher_required = role_required('teacher')
admin_required = role_required('admin')
staff_required = role_required(['admin', 'teacher'])
