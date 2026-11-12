from datetime import date
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from .forms import AppointmentForm, ContactForm
from .models import Appointment, Treatment, Testimonial

CLINIC_PHONE = '+91 98765 43210'


def home(request):
    return render(request, 'website/home.html', {
        'treatments': Treatment.objects.filter(is_featured=True)[:8],
        'testimonials': Testimonial.objects.filter(is_published=True)[:4],
    })


def about(request):
    return render(request, 'website/about.html')


def treatment_list(request):
    return render(request, 'website/treatments.html', {'treatments': Treatment.objects.all()})


def treatment_detail(request, slug):
    treatment = get_object_or_404(Treatment, slug=slug)
    return render(request, 'website/treatment_detail.html', {'treatment': treatment})


def testimonials(request):
    return render(request, 'website/testimonials.html', {'testimonials': Testimonial.objects.filter(is_published=True)})


def available_slots(request):
    raw_date = request.GET.get('date', '')
    try:
        selected_date = date.fromisoformat(raw_date)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Choose a valid date.', 'available': []}, status=400)
    if selected_date < timezone.localdate() or selected_date.weekday() == 6:
        return JsonResponse({'available': []})
    booked = set(Appointment.objects.filter(appointment_date=selected_date).exclude(status='cancelled').values_list('appointment_time', flat=True))
    all_slots = [f'{h:02d}:{m:02d}' for h in range(9, 18) for m in (0, 30)]
    if selected_date == timezone.localdate():
        now = timezone.localtime().strftime('%H:%M')
        all_slots = [s for s in all_slots if s > now]
    return JsonResponse({'available': [s for s in all_slots if s not in booked]})


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    appointment = form.save()
                request.session['last_booking_ref'] = str(appointment.booking_reference)
                return redirect('appointment_success', reference=appointment.booking_reference)
            except IntegrityError:
                form.add_error('appointment_time', 'That time has just been booked. Please select another available time.')
    else:
        form = AppointmentForm(initial={'appointment_date': timezone.localdate()})
    return render(request, 'website/book_appointment.html', {'form': form})


def appointment_success(request, reference):
    appointment = get_object_or_404(Appointment, booking_reference=reference)
    return render(request, 'website/appointment_success.html', {'appointment': appointment})


def check_appointment(request):
    appointment = None
    error = None
    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()
        phone = request.POST.get('phone', '').strip()
        try:
            appointment = Appointment.objects.get(booking_reference=reference, phone=phone)
        except (Appointment.DoesNotExist, ValueError):
            error = 'We could not find an appointment with those details. Please check and try again.'
    return render(request, 'website/check_appointment.html', {'appointment': appointment, 'error': error})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your message has been received. The clinic team will contact you.')
        return redirect('contact')
    return render(request, 'website/contact.html', {'form': form})


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')
