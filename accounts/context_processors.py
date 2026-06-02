from prayers.models import PrayerRequest
from .models import ChurchInfo


def notification_count(request):
    ctx = {}
    if request.user.is_authenticated and request.user.profile.role in ['admin', 'pastor']:
        pending = PrayerRequest.objects.filter(status='pending').count()
        ctx['pending_prayer_count'] = pending
    else:
        ctx['pending_prayer_count'] = 0
    ctx['church_info'] = ChurchInfo.get_info()
    return ctx
