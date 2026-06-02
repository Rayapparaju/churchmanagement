from django.db import models
from members.models import Staff


class Attendance(models.Model):
    EVENT_TYPES = [
        ('sunday_service', 'Sunday Service'),
        ('prayer_meeting', 'Prayer Meeting'),
        ('bible_study', 'Bible Study'),
        ('youth_meeting', 'Youth Meeting'),
        ('choir_practice', 'Choir Practice'),
        ('cell_group', 'Cell Group'),
        ('other', 'Other'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='attendance_records')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    date = models.DateField()
    attended = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'staff__first_name']
        unique_together = ['staff', 'event_type', 'date']

    def __str__(self):
        return f"{self.staff.full_name()} - {self.get_event_type_display()} ({self.date})"
