"""Event model"""
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth import get_user_model
from .validators import validate_future_date
from .customer import Customer
from .contract import Contract


User = get_user_model()


TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9]',
                            message='characters must be Alphanumeric')


class Event(models.Model):
    """Event class"""
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)
    customer_id = models.ForeignKey(to=Customer,
                                    on_delete=models.CASCADE, null=True,
                                    blank=True)
    contract_id = models.ForeignKey(to=Contract,
                                    on_delete=models.CASCADE, null=True,
                                    blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendees = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0)])
    event_date = models.DateTimeField(null=True,
                                      validators=[validate_future_date])
    notes = models.TextField(blank=True, validators=[TEXT_REGEX])
    status = models.BooleanField(default=True)


    class Meta:
        """Class meta"""
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        print("contract_id", self.contract_id)
        return str(self.contract_id) + " event"
