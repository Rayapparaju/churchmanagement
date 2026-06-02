from django.contrib import admin
from .models import Ministry


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'meeting_schedule', 'meeting_location', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'leader', 'description')
    filter_horizontal = ('members',)
