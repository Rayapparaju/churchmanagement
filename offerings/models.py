from django.db import models
from members.models import Member
from urllib.parse import quote


class Offering(models.Model):
    OFFERING_TYPES = [
        ('tithe', 'Tithe'),
        ('offering', 'Offering'),
        ('first_fruits', 'First Fruits'),
        ('thanksgiving', 'Thanksgiving'),
        ('building_fund', 'Building Fund'),
        ('mission', 'Mission'),
        ('special', 'Special Contribution'),
        ('other', 'Other'),
    ]

    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='offerings')
    offering_type = models.CharField(max_length=30, choices=OFFERING_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=30, choices=[
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('mobile_money', 'Mobile Money'),
        ('online', 'Online Payment'),
    ], default='cash')
    receipt_number = models.CharField(max_length=30, unique=True, editable=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_offering_type_display()} - ₹{self.amount} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last = Offering.objects.order_by('-id').first()
            last_id = last.id if last else 0
            self.receipt_number = f'RCP{last_id + 1:06d}'
        super().save(*args, **kwargs)

    def whatsapp_message(self):
        from accounts.models import ChurchInfo
        church = ChurchInfo.get_info()
        name = church.name if church and church.name else 'Grace Community Church'
        member_name = self.member.full_name() if self.member else 'Anonymous'
        lines = [
            f'🏛️ *{name}*',
            f'📄 Receipt: {self.receipt_number}',
            f'📅 Date: {self.date.strftime("%d %b %Y")}',
            f'👤 Member: {member_name}',
            f'📋 Type: {self.get_offering_type_display()}',
            f'💰 Amount: ₹{self.amount}',
            f'💳 Payment: {self.get_payment_method_display()}',
        ]
        if self.notes:
            lines.append(f'📝 Notes: {self.notes}')
        return '\n'.join(lines)

    def whatsapp_url(self):
        phone = self.member.phone if self.member else ''
        if not phone:
            return None
        digits = ''.join(filter(str.isdigit, phone))
        if digits.startswith('91') and len(digits) > 10:
            pass
        elif digits.startswith('0'):
            digits = '91' + digits[1:]
        elif len(digits) == 10:
            digits = '91' + digits
        return f'https://wa.me/{digits}?text={quote(self.whatsapp_message())}'
