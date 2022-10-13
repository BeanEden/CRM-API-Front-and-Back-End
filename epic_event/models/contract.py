import datetime

from django.conf import settings
from django.db import models
from .customer import Customer
from django.core.validators import validate_slug
from django.core.validators import RegexValidator
from .validators import validate_text_max_length, validate_amount, validate_future_date


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
    status = models.BooleanField(default=True)
    amount = models.FloatField(default=0, validators=[validate_amount])
    payment_due = models.DateTimeField(default=datetime.datetime.now(), validators=[validate_future_date])
    event_associated = models.CharField(max_length=20, choices=EVENT_STATUS, default="uncomplete")
    name = models.CharField(max_length=100, validators=[TEXT_REGEX], default="Contract")

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def default_name(self):
        name = "contract " + str(self.customer_id)
        number = Contract.objects.filter(customer_id=self.customer_id)
        if number:
            name = name + ' ' + str(len(number))

