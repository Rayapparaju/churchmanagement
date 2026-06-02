from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'event_type', 'date', 'attended', 'created_at']
    list_filter = ['event_type', 'attended', 'date']
    search_fields = ['staff__first_name', 'staff__last_name', 'notes']
    date_hierarchy = 'date'
    list_select_related = ['staff']
