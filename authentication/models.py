from django.contrib.auth.models import AbstractUser
from django.db import models


USER_TEAM = [('management', 'GESTION'),
             ('sales', 'VENTE'),
             ('support', 'SUPPORT')]


class User(AbstractUser):
    team = models.CharField(max_length=20, choices=USER_TEAM)
    # subscriptions = models.ManyToManyField(
    #     'self',
    #     symmetrical=False,
    #     through="review.UserFollows"
    # )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)