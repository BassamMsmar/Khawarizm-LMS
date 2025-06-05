from django.db import models
from django.utils import timezone
from department.models import Department
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
User = get_user_model()

# Create your models here.



class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200)
    lecturer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='courses_created',
        null=True,
        blank=True
    )
    academic_hours = models.IntegerField(default=0)
    short_description = models.TextField(max_length=300)
    description = CKEditor5Field('Description', blank=True, null=True)
    department = models.ManyToManyField(Department)
    image = models.ImageField(upload_to='courses/images/')
    thumbnail = models.ImageField(upload_to='courses/images/thumbnails/')
    what_youll_learn = CKEditor5Field(blank=True, null=True)
    who_this_course_is_for = CKEditor5Field(blank=True, null=True)
    students_enrolled = models.ManyToManyField(
        get_user_model(),
        related_name='enrolled_courses',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def get_enrolled_students(self):
        return self.students_enrolled.all()
    
    def get_enrolled_count(self):
        return self.students_enrolled.count()
    

class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('url', 'URL'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=200)
    description = CKEditor5Field(blank=True, null=True)
    content = CKEditor5Field(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(
        upload_to='lesson_videos/',
        blank=True,
        null=True
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes",
        default=0
    )
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPES,
        default='video'
    )
    pdf_file = models.FileField(
        upload_to='lesson_pdfs/',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='lesson_images/',
        blank=True,
        null=True
    )
    url = models.URLField(
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
