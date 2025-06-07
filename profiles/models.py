from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
User = get_user_model()

class Language(models.Model):
    """Language model for user preferences"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    """Additional profile information for students"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True, null=True)
    
    # Documents
    certificate_number = models.CharField(max_length=50, blank=True, null=True)
    certificate_file = models.FileField(upload_to='student_certificates/', blank=True, null=True)
    
    languages = models.ManyToManyField(Language, blank=True, related_name='student_profiles')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Student Profile - {self.user.username}"




class LecturerProfile(models.Model):
    """Profile information for lecturers"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='lecturer_profile'
    )
    
    headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    certification = models.TextField(blank=True, null=True)


    languages = models.ManyToManyField(Language, blank=True, related_name='lecturer_profiles')
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Lecturer Profile - {self.user.username}"
