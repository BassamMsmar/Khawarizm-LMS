from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from courses.models import Course, Lesson, Quiz
from .models import Notification
from accounts.models import User # Import User model

@receiver(post_save, sender=Course)
def create_course_notification(sender, instance, created, **kwargs):
    if created:
        # print(f"DEBUG: Course signal triggered for {instance.title}")
        students_in_department = User.objects.filter(
            profile_type='student', # Filter for students
            department=instance.department # Filter by department of the new course
        )
        # print(f"DEBUG: Found {students_in_department.count()} students in department {instance.department.name}")
        for student in students_in_department:
            Notification.objects.create(
                recipient=student,
                message=f"A new course, {instance.title}, has been added in your department ({instance.department.name}).",
                link=reverse('courses:course_detail', kwargs={'slug': instance.slug})
            )

@receiver(post_save, sender=Lesson)
def create_lesson_notification(sender, instance, created, **kwargs):
    # print(f"DEBUG: create_lesson_notification triggered for Lesson: {instance.title}, Created: {created}")
    if created:
        if instance.course: # Ensure lesson is associated with a course
            # print(f"DEBUG: Lesson is associated with course: {instance.course.title}")
            students = instance.course.students_enrolled.all()
            # print(f"DEBUG: Found {students.count()} students enrolled in course {instance.course.title}")
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    message=f"A new lesson, {instance.title}, has been added to {instance.course.title}.",
                    link=reverse('courses:lesson_detail', kwargs={'course_slug': instance.course.slug, 'lesson_slug': instance.slug})
                )
        else:
            pass
            # print(f"DEBUG: Lesson {instance.title} is NOT associated with a course.")

@receiver(post_save, sender=Quiz)
def create_quiz_notification(sender, instance, created, **kwargs):
    # print(f"DEBUG: create_quiz_notification triggered for Quiz: {instance.title}, Created: {created}")
    if created:
        if instance.unit and instance.unit.course: # Ensure quiz is associated with a unit and a course
            # print(f"DEBUG: Quiz is associated with unit: {instance.unit.title} and course: {instance.unit.course.title}")
            students = instance.unit.course.students_enrolled.all()
            # print(f"DEBUG: Found {students.count()} students enrolled in course {instance.unit.course.title}")
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    message=f"A new quiz, {instance.title}, has been added to {instance.unit.course.title}.",
                    link=reverse('courses:quiz_detail', kwargs={'course_slug': instance.unit.course.slug, 'quiz_slug': instance.slug})
                )
        else:
            pass
            # print(f"DEBUG: Quiz {instance.title} is NOT associated with a unit or course.")
