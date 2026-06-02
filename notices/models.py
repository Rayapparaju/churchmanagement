from django.db import models


class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('announcement', 'Announcement'),
        ('event', 'Event Notice'),
        ('urgent', 'Urgent'),
        ('general', 'General'),
        ('thanks', 'Thanksgiving'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
