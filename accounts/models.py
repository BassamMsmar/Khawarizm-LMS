from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.urls import reverse


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student'
    )
    phone_number = PhoneNumberField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_instructor(self):
        return self.user_type == 'instructor'

    def get_absolute_url(self):
        if self.is_instructor:
            return reverse('instructor_profile', kwargs={'username': self.username})
        return reverse('profile', kwargs={'username': self.username})


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class LecturerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)  # سنوات الخبرة
    education = models.TextField(blank=True, null=True)
    certification = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name='instructors')
    languages = models.ManyToManyField(Language, blank=True, related_name='instructors')
    available_for_consulting = models.BooleanField(default=False)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    social_links = models.JSONField(default=dict, blank=True)
    cv = models.FileField(
        upload_to='instructor_cvs/',
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    total_students = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"LecturerProfile - {self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    def update_stats(self):
        """تحديث إحصائيات المدرس مثل عدد الطلاب والدورات."""
        from courses.models import Course
        self.total_courses = Course.objects.filter(instructor=self.user).count()
        # أضف تحديثات أخرى حسب الحاجة
        self.save()
