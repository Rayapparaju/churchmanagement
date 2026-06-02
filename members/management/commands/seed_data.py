from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from members.models import Member
from ministries.models import Ministry
from events_app.models import Event
from sermons.models import Sermon
from notices.models import Notice
from prayers.models import PrayerRequest


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@church.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            self.stdout.write('Superuser "admin" already exists')

        # Members
        if Member.objects.count() < 2:
            member1, created = Member.objects.get_or_create(
                membership_id='CHR00001',
                defaults={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'gender': 'male',
                    'date_of_birth': '1990-05-15',
                    'phone': '1234567890',
                    'email': 'john@example.com',
                    'address': '123 Main St',
                    'marital_status': 'married',
                    'baptism_status': 'both',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created member: {member1.full_name()}'))

            member2, created = Member.objects.get_or_create(
                membership_id='CHR00002',
                defaults={
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'gender': 'female',
                    'date_of_birth': '1985-08-22',
                    'phone': '0987654321',
                    'email': 'jane@example.com',
                    'address': '456 Oak Ave',
                    'marital_status': 'single',
                    'baptism_status': 'water',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created member: {member2.full_name()}'))
        else:
            self.stdout.write('Members already exist')

        # Ministries
        if Ministry.objects.count() < 2:
            members = Member.objects.all()[:2]
            ministry1, created = Ministry.objects.get_or_create(
                name='Worship Team',
                defaults={
                    'description': 'Leading the congregation in worship through music and song.',
                    'leader': 'John Doe',
                    'meeting_schedule': 'Every Saturday 4:00 PM',
                    'meeting_location': 'Main Sanctuary',
                }
            )
            if created:
                if members:
                    ministry1.members.add(*members)
                self.stdout.write(self.style.SUCCESS(f'Created ministry: {ministry1.name}'))

            ministry2, created = Ministry.objects.get_or_create(
                name='Youth Ministry',
                defaults={
                    'description': 'Discipling and mentoring the youth of the church.',
                    'leader': 'Jane Smith',
                    'meeting_schedule': 'Every Friday 6:00 PM',
                    'meeting_location': 'Youth Hall',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created ministry: {ministry2.name}'))
        else:
            self.stdout.write('Ministries already exist')

        # Event
        if not Event.objects.exists():
            event = Event.objects.create(
                title='Sunday Service',
                description='Weekly Sunday worship service.',
                date=timezone.now().date() + timezone.timedelta(days=7),
                time='10:00:00',
                end_time='12:00:00',
                location='Main Sanctuary',
                organizer='Pastor John',
                status='upcoming',
            )
            self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))
        else:
            self.stdout.write('Events already exist')

        # Sermon
        if not Sermon.objects.exists():
            sermon = Sermon.objects.create(
                title='Walking in Faith',
                speaker='Pastor John',
                bible_verse='2 Corinthians 5:7',
                date=timezone.now().date(),
                description='A sermon on walking by faith and not by sight.',
                series='Faith Foundations',
            )
            self.stdout.write(self.style.SUCCESS(f'Created sermon: {sermon.title}'))
        else:
            self.stdout.write('Sermons already exist')

        # Notice
        if not Notice.objects.exists():
            notice = Notice.objects.create(
                title='Welcome to Grace Community Church',
                content='We are glad to have you join us. Stay tuned for upcoming events and announcements.',
                category='general',
                posted_by='Admin',
            )
            self.stdout.write(self.style.SUCCESS(f'Created notice: {notice.title}'))
        else:
            self.stdout.write('Notices already exist')

        # Prayer Request
        if not PrayerRequest.objects.exists():
            members = Member.objects.all()
            prayer = PrayerRequest.objects.create(
                member=members.first() if members else None,
                name='John Doe',
                email='john@example.com',
                phone='1234567890',
                request='Please pray for my family and our community.',
                status='pending',
            )
            self.stdout.write(self.style.SUCCESS(f'Created prayer request from: {prayer.name}'))
        else:
            self.stdout.write('Prayer requests already exist')

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
