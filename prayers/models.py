from django.db import models
from members.models import Member


class PrayerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('prayed', 'Prayed For'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='prayer_requests')
    name = models.CharField(max_length=100, help_text="Your name")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    request = models.TextField(help_text="Your prayer request")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Admin/Pastor notes")
    is_private = models.BooleanField(default=False, help_text="Keep this request private")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prayer from {self.name} - {self.get_status_display()}"
