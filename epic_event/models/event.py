from django.conf import settings
from django.db import models
from .customer import Customer
from django.core.validators import RegexValidator


TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9\s]',
                            message='characters must be Alphanumeric')

class Event(models.Model):
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.ForeignKey(to=Customer,
                                    on_delete=models.CASCADE, null=True,
                                    blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendees = models.IntegerField()
    event = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, RegexValidator= TEXT_REGEX)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)