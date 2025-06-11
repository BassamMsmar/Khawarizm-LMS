from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from college.models import College
from department.models import Department
from courses.models import Course

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True, null=True)

    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profiles')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profiles')
    course = models.ManyToManyField(Course, blank=True, related_name='student_profiles')

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    certificate_number = models.CharField(max_length=50, blank=True, null=True)
    certificate_file = models.FileField(upload_to='student_certificates/', blank=True, null=True)

    languages = models.ManyToManyField(Language, blank=True, related_name='student_profiles')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class LecturerProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='lecturer_profile')

    headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    certification = models.TextField(blank=True, null=True)

    colleges = models.ManyToManyField(College, blank=True, related_name='lecturer_profiles')
    departments = models.ManyToManyField(Department, blank=True, related_name='lecturer_profiles')
    courses = models.ManyToManyField(Course, blank=True, related_name='lecturer_profiles')

    languages = models.ManyToManyField(Language, blank=True, related_name='lecturer_profiles')

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
