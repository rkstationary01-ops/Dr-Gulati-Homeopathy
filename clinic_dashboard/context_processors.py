from django.utils import timezone
def clinic_dashboard_context(request):
    return {'now': timezone.localtime()}
