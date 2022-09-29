from django import forms
from epic_event import models


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['sales_contact',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'company_name'
                  ]

class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)