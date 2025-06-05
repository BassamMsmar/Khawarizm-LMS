from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import User, Role
from profiles.models import StudentProfile, LecturerProfile, DepartmentManagerProfile, CourseSupervisorProfile, AdminProfile




@receiver(post_save, sender=User)
def create_profiles_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # أنشئ بروفايلات لجميع الأدوار التي يمتلكها المستخدم عند الإنشاء
        roles = instance.roles.all()
        for role in roles:
            create_profile_for_role(instance, role.slug)

def create_profile_for_role(user, role_slug):
    """Helper function لإنشاء بروفايل بناء على دور المستخدم"""
    if role_slug == 'student':
        StudentProfile.objects.get_or_create(user=user)
    elif role_slug == 'lecturer':
        LecturerProfile.objects.get_or_create(user=user)
    elif role_slug == 'department_manager':
        DepartmentManagerProfile.objects.get_or_create(user=user)
    elif role_slug == 'course_supervisor':
        CourseSupervisorProfile.objects.get_or_create(user=user)
    elif role_slug == 'admin':
        AdminProfile.objects.get_or_create(user=user)

# إشارة ترقب التغييرات في علاقة ManyToMany الأدوار لتحديث البروفايلات حسب الإضافة أو الحذف
@receiver(m2m_changed, sender=User.roles.through)
def update_profiles_on_roles_change(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        # بعد التعديل في الأدوار، نتحقق من الأدوار الحالية
        current_roles = instance.roles.values_list('slug', flat=True)
        
        # إنشاء بروفايلات للأدوار الجديدة
        for role_slug in current_roles:
            create_profile_for_role(instance, role_slug)
        
        # هنا يمكن إضافة منطق حذف أو تعطيل البروفايلات إذا تم حذف دور معين من المستخدم
