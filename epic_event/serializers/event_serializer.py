"""Event serializer"""
from rest_framework.serializers import ModelSerializer, ChoiceField
from django.contrib.auth import get_user_model
from epic_event.models.event import Event


User = get_user_model()


def get_support_contact():
    """get support user for selection"""
    queryset = User.objects.filter(team='support')
    return queryset


class EventSerializer(ModelSerializer):
    """Event serializer"""
    support_contact = ChoiceField(choices=get_support_contact(),
                                  allow_null=True)

    class Meta:
        """Meta class"""
        model = Event
        fields = ['id',
                  'support_contact',
                  'customer_id',
                  'contract_id',
                  'attendees',
                  'event_date',
                  'notes'
                  ]
