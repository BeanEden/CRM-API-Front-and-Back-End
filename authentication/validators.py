"""Validators"""
from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """Letters validators"""
    def validate(self, password, user=None):
        """check conditions"""
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre',
                code='password_no_letters')

    def get_help_text(self):
        """return help text"""
        return 'Votre mot de passe doit contenir au moins ' \
               'une lettre majuscule ou minuscule.'


class ContainsNumberValidator:
    """Numbers validators"""
    def validate(self, password, user=None):
        """check conditions"""
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre',
                code='password_no_number')

    def get_help_text(self):
        """return help text"""
        return 'Votre mot de passe doit contenir au moins un chiffre.'
