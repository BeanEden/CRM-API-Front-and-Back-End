from django import forms

from epic_event import models

class ContractForm(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = ['sales_contact',
                  'customer_id',
                  'status',
                  'amount',
                  'payment_due'
                  ]
