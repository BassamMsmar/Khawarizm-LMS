from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

# Role choices for use in admin or other parts of the app (optional)
ROLE_CHOICES = (
    ('admin', 'Admin'),
    # ('department_manager', 'Department Manager'),
    ('lecturer', 'Lecturer'),
    # ('course_supervisor', 'Course Supervisor'),
    ('student', 'Student'),
)

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=ROLE_CHOICES)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # Many-to-many relationship to allow multiple roles per user
    roles = models.ManyToManyField(Role, blank=True)

    # USER_TYPE_CHOICES for profile 
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    @property
    def full_name(self):
        # Return the user's full name (first name + last name)
        return f"{self.first_name} {self.last_name}"

    def has_role(self, slug):
        # Check if the user has a specific role by slug
        return self.roles.filter(slug=slug).exists()
