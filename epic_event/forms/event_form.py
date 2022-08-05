from django import forms
from epic_event import models


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['support_contact',
                  'customer_id',
                  'attendees',
                  'event',
                  'notes'
                  ]
