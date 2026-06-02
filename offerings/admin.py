from django.contrib import admin
from .models import Offering


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'member', 'offering_type', 'amount', 'payment_method', 'date', 'created_at')
    list_filter = ('offering_type', 'payment_method', 'date')
    search_fields = ('receipt_number', 'member__first_name', 'member__last_name', 'notes')
    date_hierarchy = 'date'
    readonly_fields = ('receipt_number', 'created_at')
    fieldsets = (
        ('Offering Info', {
            'fields': ('member', 'offering_type', 'amount', 'date')
        }),
        ('Payment', {
            'fields': ('payment_method', 'receipt_number')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
