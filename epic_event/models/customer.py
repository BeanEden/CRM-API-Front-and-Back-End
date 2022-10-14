from django.conf import settings
from django.db import models
from django.core.validators import validate_slug
from django.core.validators import RegexValidator, MaxLengthValidator

TEXT_REGEX = RegexValidator(regex='[a-zA-Z0-9\s]',
                            message='Characters must be Alphanumeric')

PHONE_REGEX = RegexValidator(regex='[+0-9]',
                             message='Phone number must contain digits')

CUSTOMER_STATUS = [('prospect', 'PROSPECT'),
             ('ongoing', 'EN COURS'),
             ('unactive', 'NON ACTIF'),
              ('blacklisted', 'BLACKLIST')]

CUSTOMER_PROFILE = [('uncomplete', 'UNCOMPLETE'),
                    ('complete', 'COMPLETE')
             ]


class Customer(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sales_user_assigned', null=True)
    first_name = models.CharField(max_length=50, validators=[TEXT_REGEX, MaxLengthValidator(50)], blank=True)
    last_name = models.CharField(max_length=50, validators=[TEXT_REGEX], blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, validators=[PHONE_REGEX], blank=True)
    mobile = models.CharField(max_length=20, validators=[PHONE_REGEX], blank=True)
    company_name = models.CharField(max_length=200, validators=[TEXT_REGEX], blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS, default=CUSTOMER_STATUS[0][0])
    profile = models.CharField(max_length=20, choices=CUSTOMER_PROFILE, default=CUSTOMER_PROFILE[0][0])

    class Meta:
        ordering = ['-date_updated']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        if self.company_name:
            return str(self.company_name)
        name = self.first_name + ' '+self.last_name
        return str(name)

    def checking_status(self, contract_list):
        if self.status == CUSTOMER_STATUS[3][0]:
            pass
        elif len(contract_list) == 0:
            self.status = CUSTOMER_STATUS[0][0]
        else:
            ongoing_contracts = 0
            for i in contract_list:
                if i.status:
                    self.status = CUSTOMER_STATUS[1][0]
                    ongoing_contracts += 1
            if ongoing_contracts == 0:
                self.status = CUSTOMER_STATUS[2][0]
        self.save()

    def checking_profile_complete(self):
        error_message = []
        if not self.email:
            self.profile = CUSTOMER_PROFILE[0][0]
        elif not self.first_name or not self.company_name:
            self.profile = CUSTOMER_PROFILE[0][0]
        elif self.phone + self.mobile == 0:
            self.profile = CUSTOMER_PROFILE[0][0]
        else:
            self.profile = "complete"
        self.save()