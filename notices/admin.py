from django.contrib import admin
from .models import Notice


@admin.action(description='Pin selected notices')
def pin_notices(modeladmin, request, queryset):
    queryset.update(is_pinned=True)


@admin.action(description='Unpin selected notices')
def unpin_notices(modeladmin, request, queryset):
    queryset.update(is_pinned=False)


@admin.action(description='Activate selected notices')
def activate_notices(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Deactivate selected notices')
def deactivate_notices(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'is_pinned', 'posted_by', 'created_at')
    list_filter = ('category', 'is_active', 'is_pinned', 'created_at')
    search_fields = ('title', 'content', 'posted_by')
    actions = [pin_notices, unpin_notices, activate_notices, deactivate_notices]
