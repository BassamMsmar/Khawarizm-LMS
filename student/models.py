from django.db import models
from django.conf import settings

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class RegistrationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class Payment(models.Model):
    # Changed from Student to StudentProfile/User. Direct link to user avoids circular imports if Profile imports this.
    # However, to simulate 'Student' model replacement, let's link to StudentProfile or User.
    # Ideally link to User for payments.
    student = models.ForeignKey('profiles.StudentProfile', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=100)
    receipt_image = models.ImageField(upload_to='receipts/')
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.amount} - {self.status}'

class CourseRegistration(models.Model):
    student = models.ForeignKey('profiles.StudentProfile', on_delete=models.CASCADE, related_name='course_registrations')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='course_registrations')
    status = models.CharField(max_length=10, choices=RegistrationStatus.choices, default=RegistrationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.user.email} - {self.course.title} - {self.status}'
