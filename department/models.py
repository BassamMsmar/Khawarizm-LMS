from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200)

class DegreeLevel(models.Model):
    name = models.CharField(max_length=100)

class Program(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree_level = models.ForeignKey(DegreeLevel, on_delete=models.CASCADE)