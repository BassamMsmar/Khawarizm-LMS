from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student

@receiver(post_save, sender=Student)
def set_student_total_fees(sender, instance, created, **kwargs):
    if created and instance.department:
        instance.total_fees = instance.department.subscription_fee
        instance.save()
