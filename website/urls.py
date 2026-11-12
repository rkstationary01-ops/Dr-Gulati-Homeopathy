from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('treatments/', views.treatment_list, name='treatments'),
    path('treatments/<slug:slug>/', views.treatment_detail, name='treatment_detail'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/available-slots/', views.available_slots, name='available_slots'),
    path('appointments/success/<uuid:reference>/', views.appointment_success, name='appointment_success'),
    path('appointments/check/', views.check_appointment, name='check_appointment'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
