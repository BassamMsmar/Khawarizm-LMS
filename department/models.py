from django.db import models
from college.models import College

# لتحديد درجة القسم (الدكتوراه، الماجستير، البكالوريوس)
class DegreeLevel(models.Model):
    name = models.CharField(max_length=100)

# لتحديد القسم (هندسة برمجة الحاسوب، هندسة الشبكات، هندسة البرمجيات  )
class Department(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='department/images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='department/images/thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)
    degree_level = models.ForeignKey(DegreeLevel, on_delete=models.CASCADE, null=True, blank=True)

