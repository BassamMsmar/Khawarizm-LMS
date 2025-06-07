from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from .managers import UserManager

# Role choices for use in admin or other parts of the app (optional)
ROLE_CHOICES = (
    ('admin', 'Admin'),
    # ('department_manager', 'Department Manager'),
    ('staff', 'Staff'),
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


class User(AbstractBaseUser, PermissionsMixin):
    # Many-to-many relationship to allow multiple roles per user for dashboard
    roles = models.ManyToManyField('accounts.Role', blank=True)

    # USER_TYPE_CHOICES for profile 
    PROFILE_TYPE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES)

    # Basic user info
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    # Profile info
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    # Authentication fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
 
    # Override username field
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def full_name(self):
        # Return the user's full name (first name + last name)
        return f"{self.first_name} {self.last_name}"

    def has_role(self, slug):
        # Check if the user has a specific role by slug
        return self.roles.filter(slug=slug).exists()

    def save(self, *args, **kwargs):
        # Save the user first to get the ID
        super().save(*args, **kwargs)

        # After saving, handle roles and profiles
        if self.pk is None:
            if self.profile_type == 'lecturer':
                self.roles.add(Role.objects.get(name='lecturer'))
                from profiles.models import LecturerProfile
                LecturerProfile.objects.create(user=self)
            elif self.profile_type == 'student':
                self.roles.add(Role.objects.get(name='student'))
                from profiles.models import StudentProfile
                StudentProfile.objects.create(user=self)
            