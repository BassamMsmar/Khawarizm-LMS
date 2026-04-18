from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from utils.slug import get_unique_slug


class Question(models.Model):
    question = models.TextField(max_length=1000, blank=True, null=True)
    answer = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# Create your models here.
class College(models.Model):
    title = models.CharField(max_length=100 , blank=True, null=True)  # College Title
    slug = models.SlugField(unique=True, blank=True, null=True)      # College Slug
    about = models.TextField(max_length=1000, blank=True, null=True)                # About College
    max_students = models.PositiveIntegerField(default=0)  # 0 = unlimited
    is_public = models.BooleanField(default=False)
    regular_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='college_thumbnails/', null=True, blank=True)
    intro_video_url = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)  # مفصولة بفواصل
    targeted_audience = models.TextField(blank=True)
    questions = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(College, self.title, self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


