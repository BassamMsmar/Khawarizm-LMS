
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from college.models import College
from department.models import Department
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

print(f"Colleges: {College.objects.count()}")
print(f"Departments: {Department.objects.count()}")
print(f"Courses: {Course.objects.count()}")
print(f"Users: {User.objects.count()}")

for c in College.objects.all():
    print(f"College: {c.title}")
