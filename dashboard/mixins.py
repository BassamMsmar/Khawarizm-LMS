from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class RolesRequiredMixin(LoginRequiredMixin):
    allowed_roles = []  # أسماء الأدوار المسموح بها

    redirect_url = 'home'  # الوجهة عند عدم التوافق

    def dispatch(self, request, *args, **kwargs):
        # التحقق من تسجيل الدخول يتم من LoginRequiredMixin
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_roles = request.user.roles.values_list('name', flat=True)
        print("✅ user roles:", list(user_roles))
        print("🟨 allowed roles:", self.allowed_roles)

        if not set(self.allowed_roles).intersection(user_roles):
            return redirect(self.redirect_url)

        return super().dispatch(request, *args, **kwargs)