from django import forms
from django.core.exceptions import ValidationError
from website.models import Appointment, Treatment, Testimonial

class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'phone', 'email', 'treatment', 'appointment_date', 'appointment_time', 'reason', 'status']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        day = cleaned.get('appointment_date')
        slot = cleaned.get('appointment_time')
        status = cleaned.get('status')
        if day and slot and status != 'cancelled':
            conflicts = Appointment.objects.filter(appointment_date=day, appointment_time=slot).exclude(status='cancelled')
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)
            if conflicts.exists():
                self.add_error('appointment_time', 'This slot is already assigned to another active appointment.')
        return cleaned

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['title', 'slug', 'short_description', 'description', 'icon', 'is_featured', 'display_order']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['patient_name', 'quote', 'rating', 'is_published']
        widgets = {'quote': forms.Textarea(attrs={'rows': 4})}
