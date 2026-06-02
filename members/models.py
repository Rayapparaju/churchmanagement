from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    BAPTISM_CHOICES = [
        ('water', 'Water Baptism'),
        ('holy_spirit', 'Holy Spirit Baptism'),
        ('both', 'Both'),
        ('none', 'None'),
    ]
    MARITAL_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    membership_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='member_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, default='single')
    baptism_status = models.CharField(max_length=20, choices=BAPTISM_CHOICES, default='none')
    baptism_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField(default=date.today)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    family_head = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='family_members')
    is_active = models.BooleanField(default=True)
    is_voter = models.BooleanField(default=False, verbose_name='Registered Voter')
    voter_id = models.CharField(max_length=50, blank=True, verbose_name='Voter ID / EPIC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_id})"

    def save(self, *args, **kwargs):
        if not self.membership_id:
            last = Member.objects.order_by('-id').first()
            last_id = last.id if last else 0
            self.membership_id = f'CHR{last_id + 1:05d}'
        super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BaptismCertificate(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='baptism_certificates')
    certificate_number = models.CharField(max_length=30, unique=True, editable=False)
    baptism_date = models.DateField()
    baptism_type = models.CharField(max_length=20, choices=Member.BAPTISM_CHOICES, default='water')
    officiated_by = models.CharField(max_length=200, blank=True, verbose_name='Officiated By (Pastor)')
    date_issued = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-baptism_date']
        verbose_name = 'Baptism Certificate'
        verbose_name_plural = 'Baptism Certificates'

    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.member.full_name()}"

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            last = BaptismCertificate.objects.order_by('-id').first()
            last_id = last.id if last else 0
            self.certificate_number = f'BC{last_id + 1:05d}'
        super().save(*args, **kwargs)


class Staff(models.Model):
    STAFF_ROLES = [
        ('pastor', 'Pastor'),
        ('associate_pastor', 'Associate Pastor'),
        ('youth_pastor', 'Youth Pastor'),
        ('worship_leader', 'Worship Leader'),
        ('administrator', 'Administrator'),
        ('secretary', 'Secretary'),
        ('teacher', 'Teacher'),
        ('volunteer', 'Volunteer'),
        ('deacon', 'Deacon'),
        ('elder', 'Elder'),
    ]
    staff_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=STAFF_ROLES)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    ministry = models.ForeignKey('ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            last = Staff.objects.order_by('-id').first()
            last_id = last.id if last else 0
            self.staff_id = f'STF{last_id + 1:05d}'
        super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
