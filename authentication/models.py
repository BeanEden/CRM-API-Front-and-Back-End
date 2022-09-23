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
    username = models.CharField(max_length=255, validators=[validate_slug],
                                unique=True)
    password = models.CharField(max_length=255, blank=False,
                                validators=[validate_password])

    def __str__(self):
        return str(self.username)



def clean_string(string, *args):
    """Clean strings (delete characters) in order to get a proper username
    Args :
    - string to modify
    - args (characters to delete)
    Return : string without selected characters"""
    string = string.casefold()
    for i in args:
        string = string.replace(i, "")
    return string


def set_username(instance, **kwargs):
    """ Function used to create a username
    Not a method of User
    Args : user instance
    Return: Add an username to the User, first_name-last_name(
    +number if already existing)"""
    if not instance.username:
        clean_first_name = clean_string(instance.first_name, " ", "-")
        clean_last_name = clean_string(instance.last_name, " ", "-")
        username = clean_first_name + "_" + clean_last_name
        counter = 1
        while User.objects.filter(username=username):
            username = username + str(counter)
            counter += 1
        instance.username = username


models.signals.pre_save.connect(set_username, sender=User)