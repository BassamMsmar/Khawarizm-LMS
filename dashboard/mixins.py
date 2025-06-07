from django.shortcuts import redirect
from django.views import View

class UserTypeRedirectMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        # نحصل على نوع المستخدم المطلوب للعرض الحالي
        required_user_type = getattr(self, 'required_user_type', None)

        if required_user_type and user.roles != required_user_type:
            # إعادة التوجيه حسب نوع المستخدم الحالي
            if user.roles == 'student':
                return redirect('dashboard:student:studentDashboard')
            elif user.roles == 'staff':
                return redirect('dashboard:staff:staffDashboard')
            elif user.user_type == 'admin':
                return redirect('dashboard:admin:adminDashboard')
            else:
                # للمستخدمين غير معروفين أو أنواع أخرى، يمكن إعادة توجيه عام
                return redirect('login')

        return super().dispatch(request, *args, **kwargs)
