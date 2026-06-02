from django.db import models


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    speaker = models.CharField(max_length=100)
    bible_verse = models.CharField(max_length=100, blank=True, help_text="e.g., John 3:16")
    date = models.DateField()
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='sermon_files/audio/', blank=True, null=True)
    video_link = models.URLField(blank=True, help_text="YouTube or other video link")
    document = models.FileField(upload_to='sermon_files/documents/', blank=True, null=True)
    series = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.speaker} ({self.date})"
