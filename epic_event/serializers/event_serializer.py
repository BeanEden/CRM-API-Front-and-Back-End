from rest_framework.serializers import ModelSerializer, ChoiceField,ReadOnlyField ,SerializerMethodField
from django.contrib.auth import get_user_model
from epic_event.models.event import Event
User = get_user_model()
#
# def support_contact_choice():
#     support_choice = User.objects.filter(team="support")
#     return support_choice
#
#
# CHOICES = support_contact_choice()

class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id',
                 'support_contact',
                 'customer_id',
                 'contract_id',
                 'attendees',
                 'event_date',
                 'notes'
                 ]

        extra_kwargs = {
            'contract_id' : {'read_only': True},
            'customer_id' : {'read_only': True},

        }

