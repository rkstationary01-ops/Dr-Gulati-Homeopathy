import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class Treatment(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=30, default='✚')
    is_featured = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    patient_name = models.CharField(max_length=100)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.patient_name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    SLOT_CHOICES = [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(9, 18) for m in (0, 30)]
    booking_reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^[0-9+\- ]{8,15}$', 'Enter a valid phone number.')])
    email = models.EmailField(blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=5, choices=SLOT_CHOICES)
    reason = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', 'appointment_time']
        constraints = [
            models.UniqueConstraint(fields=['appointment_date', 'appointment_time'], condition=~models.Q(status='cancelled'), name='unique_active_appointment_slot')
        ]

    def __str__(self):
        return f'{self.patient_name} - {self.appointment_date} {self.appointment_time}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.created_at:%d-%m-%Y})'
