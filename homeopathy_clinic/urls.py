from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Original Django admin remains available.
    path('clinic-admin/', include('clinic_dashboard.urls')),  # Separate custom staff dashboard.
    path('', include('website.urls')),  # Existing public website routes remain unchanged.
]
