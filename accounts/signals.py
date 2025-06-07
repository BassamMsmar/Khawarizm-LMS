from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from profiles.models import StudentProfile, LecturerProfile




@receiver(post_save, sender=User)
def create_profiles_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # أنشئ بروفايلات لجميع الأدوار التي يمتلكها المستخدم عند الإنشاء
        if instance.user_type == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'lecturer':
            LecturerProfile.objects.get_or_create(user=instance)
