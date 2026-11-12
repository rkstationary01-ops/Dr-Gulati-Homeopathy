from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Appointment, ContactMessage

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'phone', 'email', 'treatment', 'appointment_date', 'appointment_time', 'reason']
        widgets = {
            'patient_name': forms.TextInput(attrs={'placeholder': 'Your full name', 'autocomplete': 'name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Mobile number', 'autocomplete': 'tel'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address (optional)', 'autocomplete': 'email'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.localdate().isoformat()}),
            'appointment_time': forms.Select(attrs={'id': 'id_appointment_time'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Briefly tell us what you would like to discuss (optional)'}),
        }

    def clean_appointment_date(self):
        value = self.cleaned_data['appointment_date']
        if value < timezone.localdate():
            raise forms.ValidationError('Please choose today or a future date.')
        if value.weekday() == 6:
            raise forms.ValidationError('The clinic is closed on Sundays. Please choose another date.')
        return value

    def clean(self):
        cleaned = super().clean()
        selected_date = cleaned.get('appointment_date')
        selected_time = cleaned.get('appointment_time')
        if selected_date and selected_time:
            if selected_date == timezone.localdate():
                now = timezone.localtime().strftime('%H:%M')
                if selected_time <= now:
                    self.add_error('appointment_time', 'Please choose a future time.')
            if Appointment.objects.filter(appointment_date=selected_date, appointment_time=selected_time).exclude(status='cancelled').exists():
                self.add_error('appointment_time', 'This time slot is already booked. Please choose another time.')
        return cleaned

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'How can we help you?'})}
