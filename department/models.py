from django.db import models
from college.models import College

# لتحديد درجة القسم (الدكتوراه، الماجستير، البكالوريوس)
class DegreeLevel(models.Model):
    name = models.CharField(max_length=100)

# لتحديد القسم (هندسة برمجة الحاسوب، هندسة الشبكات، هندسة البرمجيات  )
class Department(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='department/images/')
    thumbnail = models.ImageField(upload_to='department/images/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    degree_level = models.ForeignKey(DegreeLevel, on_delete=models.CASCADE)

