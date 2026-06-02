from django.db import models


class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.CharField(max_length=100, blank=True)
    meeting_schedule = models.CharField(max_length=200, blank=True)
    meeting_location = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField('members.Member', blank=True, related_name='ministries')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Ministries'
        ordering = ['name']

    def __str__(self):
        return self.name
