from django.conf import settings
from django.db import models
from .customer import Customer
from .contract import Contract
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
User = get_user_model()


TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9\s]',
                            message='characters must be Alphanumeric')

class Event(models.Model):
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.ForeignKey(to=Customer,
                                    on_delete=models.CASCADE, null=True,
                                    blank=True)
    contract_id = models.ForeignKey(to=Contract,
                                    on_delete=models.CASCADE, null=True,
                                    blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(blank=True, validators=[TEXT_REGEX])

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        print("contract_id", self.contract_id.name)
        return str(self.contract_id) +" event"

