from django.conf import settings
from django.db import models
from django.core.validators import validate_slug


class Customer(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sales_user_assigned')
    first_name = models.CharField(max_length=25, validators=validate_slug)
    last_name = models.CharField(max_length=25, validators=validate_slug)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=25, validators=validate_slug)
    mobile = models.CharField(max_length=25, validators=validate_slug)
    company_name = models.CharField(max_length=25, validators=validate_slug)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)




#
# class UserFollows(models.Model):
#     """relationship between two users (followed/following)
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
