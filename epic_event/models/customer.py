from django.conf import settings
from django.db import models
from django.core.validators import validate_slug


CUSTOMER_STATUS = [('prospect', 'PROSPECT'),
             ('ongoing', 'EN COURS'),
             ('unactive', 'NON ACTIF'),
              ('blacklisted', 'BLACKLIST')]

CUSTOMER_PROFILE = [('complete', 'COMPLETE'),
             ('uncomplete', 'UNCOMPLETE')]


class Customer(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sales_user_assigned')
    first_name = models.CharField(max_length=25, validators=[validate_slug], blank=True)
    last_name = models.CharField(max_length=25, validators=[validate_slug], blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, validators=[validate_slug], blank=True)
    mobile = models.CharField(max_length=25, validators=[validate_slug], blank=True)
    company_name = models.CharField(max_length=25, validators=[validate_slug], blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS, default="prospect")
    profile = models.CharField(max_length=20, choices=CUSTOMER_PROFILE, default="uncomplete")

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)






#
# class UserFollows(models.Model):
#     """relationship between two serializers (followed/following)
#     linked in ManytoManyfield to User.subscriptions
#     (list of all people followed by the user)"""
#
#     user = models.ForeignKey(
#         to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#         related_name='following')
#     followed_user = models.ForeignKey(
#         to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#         related_name='followed_by')
#
#     class Meta:
#         unique_together = ('user', 'followed_user')
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
