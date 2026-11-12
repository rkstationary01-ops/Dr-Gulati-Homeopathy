from django.urls import path
from . import views

app_name = 'clinic_dashboard'
urlpatterns = [
    path('login/', views.StaffLoginView.as_view(), name='login'),
    path('forbidden/', views.forbidden, name='forbidden'),
    path('', views.dashboard_home, name='dashboard'),
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('patients/', views.patient_list, name='patients'),
    path('treatments/', views.treatment_list, name='treatments'),
    path('treatments/add/', views.treatment_create, name='treatment_add'),
    path('treatments/<int:pk>/edit/', views.treatment_edit, name='treatment_edit'),
    path('treatments/<int:pk>/delete/', views.treatment_delete, name='treatment_delete'),
    path('testimonials/', views.testimonial_list, name='testimonials'),
    path('testimonials/add/', views.testimonial_create, name='testimonial_add'),
    path('testimonials/<int:pk>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),
    path('enquiries/', views.enquiry_list, name='enquiries'),
    path('enquiries/<int:pk>/', views.enquiry_detail, name='enquiry_detail'),
    path('logout/', views.logout_view, name='logout'),
]
