from django.conf import settings
from django.db import models
from .customer import Customer

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
    payment_due = models.DateTimeField()
    # event = models.CharField(max_length=20, choices=CUSTOMER_PROFILE, default="uncomplete")

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)