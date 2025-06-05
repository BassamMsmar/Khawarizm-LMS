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


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    bio = models.TextField(blank=True, null=True)


class CollegeManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='college_manager_profile')
    bio = models.TextField(blank=True, null=True)

class DepartmentManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_manager_profile')
    bio = models.TextField(blank=True, null=True)

class CourseSupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='course_supervisor_profile')
    bio = models.TextField(blank=True, null=True)

class StudentProfile(models.Model):
    """Additional profile information for students"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True, null=True)
    # Education
    education_level = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    
    # Documents
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    certificate_number = models.CharField(max_length=50, blank=True, null=True)
    certificate_file = models.FileField(upload_to='student_certificates/', blank=True, null=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = PhoneNumberField(blank=True, null=True)
    
    # Additional Information
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)
    
    # Timestamps
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
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    available_for_consulting = models.BooleanField(default=False)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # Relations
    languages = models.ManyToManyField(Language, blank=True, related_name='lecturer_profiles')
    

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Lecturer Profile - {self.user.username}"
    
    def update_stats(self):
        """Update lecturer's statistics"""
        from courses.models import Course
        self.total_courses = Course.objects.filter(instructor=self.user).count()
        self.save()


# Signal to create StudentProfile when User is created
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Create a StudentProfile when a User is created with user_type='student'"""
    if created and instance.roles.filter(slug='student').exists():
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    """Save the StudentProfile when the User is saved"""
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()


