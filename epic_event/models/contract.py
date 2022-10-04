import datetime

from django.conf import settings
from django.db import models
from .customer import Customer
from django.core.validators import validate_slug
from django.core.validators import RegexValidator


TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9\s]',
                            message='characters must be Alphanumeric')

EVENT_STATUS = [('complete', 'COMPLETE'),
             ('uncomplete', 'UNCOMPLETE')]

class Contract(models.Model):
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(default=False)
    payment_due = models.DateTimeField(default=datetime.datetime.now())
    event_associated = models.CharField(max_length=20, choices=EVENT_STATUS, default="uncomplete")
    name = models.CharField(max_length=25, validators=[TEXT_REGEX], blank=True)

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
