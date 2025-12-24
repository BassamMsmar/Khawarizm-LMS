from django.db import models

# Create your models here.


class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title", null=True, blank=True)
    sub_title = models.CharField(max_length=200, verbose_name="Sub Title", null=True, blank=True)
    image = models.ImageField(upload_to='about/images', verbose_name="Image", null=True, blank=True)
    video = models.FileField(upload_to='about/videos', verbose_name="Video", null=True, blank=True)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    content = models.TextField(verbose_name="Content", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title
