"""Contract model"""
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from .validators import validate_future_date
from .customer import Customer



TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9]',
                            message='characters must be Alphanumeric')

EVENT_STATUS = [('complete', 'COMPLETE'),
                ('uncomplete', 'UNCOMPLETE')]


class Contract(models.Model):
    """Contract model"""
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE)
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    payment_due = models.DateTimeField(null=True,
                                       validators=[validate_future_date])
    event_associated = models.CharField(max_length=20, choices=EVENT_STATUS,
                                        default="uncomplete")
    name = models.CharField(max_length=100, validators=[TEXT_REGEX],
                            default="Contract")

    class Meta:
        """Meta class added for ordering"""
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
