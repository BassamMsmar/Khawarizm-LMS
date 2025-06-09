from django.db import models
from college.models import College
from django.utils.text import slugify
from utils.slug import get_unique_slug
from django.contrib.auth import get_user_model
User = get_user_model()

# لتحديد درجة القسم (الدكتوراه، الماجستير، البكالوريوس)
class DegreeLevel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(DegreeLevel, self.name, self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# لتحديد القسم (هندسة برمجة الحاسوب، هندسة الشبكات، هندسة البرمجيات  )
class Department(models.Model):
    name = models.CharField(max_length=200)
    degree_level = models.ForeignKey(DegreeLevel, on_delete=models.SET_NULL, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_admin')
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='department/images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='department/images/thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(Department, self.name, self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

