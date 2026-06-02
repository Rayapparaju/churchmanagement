from django.contrib import admin
from .models import Member, Staff, BaptismCertificate


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'first_name', 'last_name', 'gender', 'phone', 'email', 'is_active', 'joining_date')
    list_filter = ('is_active', 'gender', 'marital_status', 'baptism_status')
    search_fields = ('membership_id', 'first_name', 'last_name', 'phone', 'email')
    list_editable = ('is_active',)
    readonly_fields = ('membership_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('membership_id', 'user', 'first_name', 'last_name', 'photo')
        }),
        ('Personal Info', {
            'fields': ('gender', 'date_of_birth', 'phone', 'email', 'address', 'occupation')
        }),
        ('Family & Status', {
            'fields': ('marital_status', 'baptism_status', 'baptism_date', 'family_head')
        }),
        ('Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Membership', {
            'fields': ('joining_date', 'is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BaptismCertificate)
class BaptismCertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'member', 'baptism_date', 'baptism_type', 'date_issued')
    list_filter = ('baptism_type', 'baptism_date')
    search_fields = ('certificate_number', 'member__first_name', 'member__last_name')
    readonly_fields = ('certificate_number', 'date_issued')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'first_name', 'last_name', 'role', 'ministry', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'role', 'ministry')
    search_fields = ('staff_id', 'first_name', 'last_name', 'phone', 'email')
    list_editable = ('is_active',)
    readonly_fields = ('staff_id', 'joined_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('staff_id', 'user', 'first_name', 'last_name', 'photo')
        }),
        ('Role & Ministry', {
            'fields': ('role', 'ministry')
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Status', {
            'fields': ('joined_date', 'is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
