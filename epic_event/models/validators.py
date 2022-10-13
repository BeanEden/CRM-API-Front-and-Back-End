from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

def validate_attendees(value):
    if value <= 0:
        raise ValidationError(
            _('At least 1 attendee is required'),
            params={'value': value},
        )

def validate_amount(value):
    if value < 0:
        raise ValidationError(
            _('Amount must be at least 0'),
            params={'value': value},
        )

def validate_future_date(value):
    value = date_str_split(str(value))
    now = datetime.datetime.now()
    now = date_str_split(now)
    if value <= now:
        raise ValidationError(
            _('This date must be set in the future'),
            params={'value': value},
        )


def date_str_split(date):
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)


def validate_text_max_length(text):
    if len(text) > 100:
        raise ValidationError(
            _('At least 1 attendee is required'),
            params={'text': text},
        )