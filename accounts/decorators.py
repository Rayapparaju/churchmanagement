from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            profile = request.user.profile
            if profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admin access required.")
    return _wrapped_view


def pastor_or_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.profile.role in ['admin', 'pastor']:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Pastor or Admin access required.")
    return _wrapped_view
