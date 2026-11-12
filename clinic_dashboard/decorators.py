from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

def staff_member_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url='clinic_dashboard:login')
        if not user.is_active or not user.is_staff:
            raise PermissionDenied('Staff access is required to use the clinic dashboard.')
        return view_func(request, *args, **kwargs)
    return _wrapped
