from django.contrib import admin
from .models import Treatment, Testimonial, Appointment, ContactMessage

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'display_order')
    list_editable = ('is_featured', 'display_order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone', 'appointment_date', 'appointment_time', 'status', 'booking_reference')
    list_filter = ('status', 'appointment_date', 'treatment')
    search_fields = ('patient_name', 'phone', 'email', 'booking_reference')
    list_editable = ('status',)
    readonly_fields = ('booking_reference', 'created_at')
    date_hierarchy = 'appointment_date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'rating', 'is_published', 'created_at')
    list_editable = ('is_published',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
