from django.db import models
from django.utils import timezone
from department.models import Department
from django.contrib.auth import get_user_model
from django.urls import reverse
from utils.slug import get_unique_slug
from django_ckeditor_5.fields import CKEditor5Field
User = get_user_model()
from django.utils.text import slugify

from college.models import College

# Create your models here.



class Course(models.Model):
    title = models.CharField(max_length=100)
    lecturer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='courses_created',
        null=True,
        blank=True
    )
    academic_hours = models.IntegerField(blank=True, null=True)
    short_description = models.TextField(max_length=1000, blank=True, null=True)
    description = CKEditor5Field('Description', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='courses/images/thumbnails/', blank=True, null=True)
    what_youll_learn = CKEditor5Field(blank=True, null=True)
    who_this_course_is_for = CKEditor5Field(blank=True, null=True)
    students_enrolled = models.ManyToManyField(
        get_user_model(),
        related_name='enrolled_courses',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(Course, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def get_enrolled_students(self):
        return self.students_enrolled.all()
    
    def get_enrolled_count(self):
        return self.students_enrolled.count()
    



    # _________________________________________________________________________________________

class Unit(models.Model):
    title = models.CharField(max_length=40)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")
    slug = models.SlugField(unique=True, max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Unit, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# _________________________________________________________________________________________




class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('url', 'URL'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)

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
    order = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    completed_by = models.ManyToManyField(
        User,
        related_name='completed_lessons',
        blank=True
    )
    
    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(Lesson, self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title




class Quiz(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=150, null=True, blank=True)

    def __str__(self):
        return f"Quiz for Unit {self.unit}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Quiz, self.title)
        super().save(*args, **kwargs)


# _________________________________________________________________________________________


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.text

# _________________________________________________________________________________________


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
    
# _________________________________________________________________________________________


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField()
    comment = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.comment[:20]} for course {self.course}"
