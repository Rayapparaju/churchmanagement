from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('members/', include('members.urls')),
    path('attendance/', include('attendance.urls')),
    path('offerings/', include('offerings.urls')),
    path('events/', include('events_app.urls')),
    path('ministries/', include('ministries.urls')),
    path('sermons/', include('sermons.urls')),
    path('prayers/', include('prayers.urls')),
    path('notices/', include('notices.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
