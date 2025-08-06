from django.db import models
from django.utils.text import slugify
from college.models import College
from django.contrib.auth import get_user_model

# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='maindashboard_departments') # Added related_name
    admin = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_departments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Department, self).save(*args, **kwargs)
