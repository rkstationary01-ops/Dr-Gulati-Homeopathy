from datetime import timedelta
from functools import wraps
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from website.models import Appointment, Treatment, Testimonial, ContactMessage
from .decorators import staff_member_required
from .forms import AppointmentAdminForm, TreatmentForm, TestimonialForm

class StaffLoginView(LoginView):
    template_name = 'clinic_dashboard/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_staff and self.request.user.is_active:
            return '/clinic-admin/'
        return '/clinic-admin/forbidden/'

@staff_member_required
def forbidden(request):
    return render(request, 'clinic_dashboard/forbidden.html', status=403)

@staff_member_required
def dashboard_home(request):
    today = timezone.localdate()
    start = today - timedelta(days=6)
    appointments = Appointment.objects.select_related('treatment')
    week_rows = (appointments.filter(appointment_date__gte=start, appointment_date__lte=today)
                 .values('appointment_date').annotate(total=Count('id')).order_by('appointment_date'))
    counts = {row['appointment_date']: row['total'] for row in week_rows}
    week_values = [counts.get(start + timedelta(days=i), 0) for i in range(7)]
    week_max = max(week_values, default=0) or 1
    week = [{'label': (start + timedelta(days=i)).strftime('%a'), 'total': week_values[i], 'height_pct': max(3, round(week_values[i] / week_max * 100))} for i in range(7)]
    context = {
        'total_appointments': appointments.count(),
        'confirmed_count': appointments.filter(status='confirmed').count(),
        'pending_count': appointments.filter(status='pending').count(),
        'cancelled_count': appointments.filter(status='cancelled').count(),
        'patient_count': appointments.values('phone').distinct().count(),
        'treatment_count': Treatment.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_appointments': appointments.order_by('-created_at')[:7],
        'week': week,
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    return render(request, 'clinic_dashboard/dashboard.html', context)

@staff_member_required
def appointment_list(request):
    qs = Appointment.objects.select_related('treatment').all()
    search = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    if search:
        qs = qs.filter(Q(patient_name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(booking_reference__icontains=search))
    if status in dict(Appointment.STATUS_CHOICES):
        qs = qs.filter(status=status)
    return render(request, 'clinic_dashboard/appointments.html', {'appointments': qs[:250], 'q': search, 'selected_status': status, 'status_choices': Appointment.STATUS_CHOICES})

@staff_member_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('treatment'), pk=pk)
    if request.method == 'POST':
        form = AppointmentAdminForm(request.POST, instance=appointment)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Appointment updated successfully.')
                return redirect('clinic_dashboard:appointment_detail', pk=appointment.pk)
            except IntegrityError:
                form.add_error('appointment_time', 'This slot was booked by another request. Choose a different time.')
    else:
        form = AppointmentAdminForm(instance=appointment)
    return render(request, 'clinic_dashboard/appointment_detail.html', {'appointment': appointment, 'form': form})

@staff_member_required
def patient_list(request):
    # Patient records are derived from the existing appointments table; no duplicate patient model is introduced.
    rows = Appointment.objects.values('patient_name', 'phone', 'email').annotate(
        total_bookings=Count('id')).order_by('patient_name')
    search = request.GET.get('q', '').strip()
    if search:
        rows = rows.filter(Q(patient_name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search))
    return render(request, 'clinic_dashboard/patients.html', {'patients': rows[:250], 'q': search})

@staff_member_required
def treatment_list(request):
    return render(request, 'clinic_dashboard/treatments.html', {'treatments': Treatment.objects.all()})

@staff_member_required
def treatment_create(request):
    form = TreatmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Treatment created.'); return redirect('clinic_dashboard:treatments')
    return render(request, 'clinic_dashboard/treatment_form.html', {'form': form, 'page_title': 'Add treatment'})

@staff_member_required
def treatment_edit(request, pk):
    obj = get_object_or_404(Treatment, pk=pk)
    form = TreatmentForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Treatment updated.'); return redirect('clinic_dashboard:treatments')
    return render(request, 'clinic_dashboard/treatment_form.html', {'form': form, 'page_title': 'Edit treatment'})

@staff_member_required
@require_POST
def treatment_delete(request, pk):
    obj = get_object_or_404(Treatment, pk=pk); obj.delete()
    messages.success(request, 'Treatment deleted.'); return redirect('clinic_dashboard:treatments')

@staff_member_required
def testimonial_list(request):
    return render(request, 'clinic_dashboard/testimonials.html', {'testimonials': Testimonial.objects.all()})

@staff_member_required
def testimonial_create(request):
    form = TestimonialForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Testimonial created.'); return redirect('clinic_dashboard:testimonials')
    return render(request, 'clinic_dashboard/testimonial_form.html', {'form': form, 'page_title': 'Add testimonial'})

@staff_member_required
def testimonial_edit(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Testimonial updated.'); return redirect('clinic_dashboard:testimonials')
    return render(request, 'clinic_dashboard/testimonial_form.html', {'form': form, 'page_title': 'Edit testimonial'})

@staff_member_required
@require_POST
def testimonial_delete(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk); obj.delete()
    messages.success(request, 'Testimonial deleted.'); return redirect('clinic_dashboard:testimonials')

@staff_member_required
def enquiry_list(request):
    qs = ContactMessage.objects.all()
    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(message__icontains=search))
    return render(request, 'clinic_dashboard/enquiries.html', {'enquiries': qs[:250], 'q': search})

@staff_member_required
def enquiry_detail(request, pk):
    obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        obj.is_read = True; obj.save(update_fields=['is_read'])
        messages.success(request, 'Enquiry marked as read.')
        return redirect('clinic_dashboard:enquiries')
    return render(request, 'clinic_dashboard/enquiry_detail.html', {'enquiry': obj})

@staff_member_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('clinic_dashboard:login')
