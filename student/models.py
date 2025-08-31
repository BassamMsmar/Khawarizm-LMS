from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, null=True, blank=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.email

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.student.user.username}"