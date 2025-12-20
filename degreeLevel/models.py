from django.db import models
from django.db import models
from utils.slug import get_unique_slug

from courses.models import Course
from department.models import Department
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class DegreeLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='degree_level/images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='degree_level/images/thumbnails/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(DegreeLevel, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
