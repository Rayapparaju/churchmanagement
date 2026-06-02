from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'location', 'organizer', 'status', 'created_at']
    list_filter = ['status', 'date', 'location']
    search_fields = ['title', 'description', 'location', 'organizer', 'notes']
    filter_horizontal = ['volunteers']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'location', 'organizer', 'status')
        }),
        ('Date & Time', {
            'fields': ('date', 'time', 'end_time')
        }),
        ('Volunteers', {
            'fields': ('volunteers',)
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
