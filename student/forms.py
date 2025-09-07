from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'reference_number', 'receipt_image']  # الحقول اللي الطالب يدخلها

