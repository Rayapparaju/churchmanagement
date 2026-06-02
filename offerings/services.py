from twilio.rest import Client
from django.conf import settings


def send_whatsapp(offering, custom_message=None):
    from accounts.models import ChurchInfo

    church = ChurchInfo.get_info()
    sid = church.twilio_account_sid or getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    token = church.twilio_auth_token or getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_ = church.twilio_whatsapp_from or getattr(settings, 'TWILIO_WHATSAPP_FROM', '')

    if not all([sid, token, from_]):
        return {'success': False, 'error': 'Twilio credentials not configured.'}

    member = offering.member
    if not member or not member.phone:
        return {'success': False, 'error': 'Member has no phone number.'}

    digits = ''.join(filter(str.isdigit, member.phone))
    if digits.startswith('91') and len(digits) > 10:
        pass
    elif digits.startswith('0'):
        digits = '91' + digits[1:]
    elif len(digits) == 10:
        digits = '91' + digits
    to_number = f'whatsapp:+{digits}'

    msg = custom_message or offering.whatsapp_message()

    try:
        client = Client(sid, token)
        message = client.messages.create(
            body=msg,
            from_=f'whatsapp:{from_}',
            to=to_number,
        )
        return {'success': True, 'sid': message.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}
