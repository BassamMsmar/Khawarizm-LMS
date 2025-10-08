from django.shortcuts import render, redirect, get_object_or_404
from student.models import Payment
from accounts.decorators import staff_required


@staff_required
def payment_requests(request):
    pending_payments = Payment.objects.filter(status='pending').order_by('-created_at')
    other_payments = Payment.objects.exclude(status='pending').order_by('-created_at')
    context = {
        'pending_payments': pending_payments,
        'other_payments': other_payments,
    }
    return render(request, 'pages/payment_requests.html', context)


@staff_required
def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'approved'
    payment.save()
    return redirect('payment_requests')


@staff_required
def reject_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')
        if reason:
            payment.status = 'rejected'
            payment.rejection_reason = reason
            payment.save()
            return redirect('payment_requests')

    context = {
        'payment': payment,
    }
    return render(request, 'pages/reject_payment.html', context)
