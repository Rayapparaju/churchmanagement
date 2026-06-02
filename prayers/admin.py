from django.contrib import admin
from .models import PrayerRequest


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'request', 'status', 'is_private', 'created_at')
    list_filter = ('status', 'is_private', 'created_at')
    search_fields = ('name', 'email', 'request', 'admin_notes')
    actions = ['mark_as_prayed', 'mark_as_answered']

    def mark_as_prayed(self, request, queryset):
        updated = queryset.update(status='prayed')
        self.message_user(request, f'{updated} prayer request(s) marked as prayed.')
    mark_as_prayed.short_description = 'Mark selected as Prayed For'

    def mark_as_answered(self, request, queryset):
        updated = queryset.update(status='answered')
        self.message_user(request, f'{updated} prayer request(s) marked as answered.')
    mark_as_answered.short_description = 'Mark selected as Answered'
