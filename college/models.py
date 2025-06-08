from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)
    description = models.TextField('Description', blank=True)
    image = models.ImageField(upload_to='college/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='college/images/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    