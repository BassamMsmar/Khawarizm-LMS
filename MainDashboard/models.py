from django.db import models

class Unit(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='maindashboard_units', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# Create your models here.