"""Validators"""
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_future_date(value):
    """Validate that the selected date is in the future"""
    value = date_str_split(str(value))
    now = datetime.datetime.now()
    now = date_str_split(now)
    if value <= now:
        raise ValidationError(
            _('This date must be set in the future'),
            params={'value': value},
            )


def date_str_split(date):
    """Date reformat for comparison"""
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)
