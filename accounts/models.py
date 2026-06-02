from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pastor', 'Pastor'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ChurchInfo(models.Model):
    name = models.CharField(max_length=200, default='Grace Community Church')
    tagline = models.CharField(max_length=300, blank=True, help_text='Short tagline or mission statement')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='church_logos/', blank=True, null=True)
    description = models.TextField(blank=True, help_text='About the church')
    founded_date = models.DateField(null=True, blank=True)
    service_times = models.TextField(blank=True, help_text='Service schedule/timings')
    facebook = models.URLField(blank=True, verbose_name='Facebook URL')
    twitter = models.URLField(blank=True, verbose_name='Twitter URL')
    instagram = models.URLField(blank=True, verbose_name='Instagram URL')
    youtube = models.URLField(blank=True, verbose_name='YouTube URL')
    updated_at = models.DateTimeField(auto_now=True)

    # Twilio WhatsApp settings
    twilio_account_sid = models.CharField(max_length=100, blank=True, verbose_name='Twilio Account SID')
    twilio_auth_token = models.CharField(max_length=100, blank=True, verbose_name='Twilio Auth Token')
    twilio_whatsapp_from = models.CharField(max_length=20, blank=True, verbose_name='WhatsApp Sender Number',
                                            help_text='Twilio WhatsApp-enabled number e.g. +14155238886')

    class Meta:
        verbose_name = 'Church Information'
        verbose_name_plural = 'Church Information'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_info(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
