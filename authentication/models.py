from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_slug
from django.contrib.auth.password_validation import validate_password



USER_TEAM = [('management', 'GESTION'),
             ('sales', 'VENTE'),
             ('support', 'SUPPORT')]


class User(AbstractUser):
    team = models.CharField(max_length=20, choices=USER_TEAM)
    first_name = models.CharField(max_length=255, validators=[validate_slug])
    last_name = models.CharField(max_length=255, validators=[validate_slug])
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False,
                                validators=[validate_password])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)