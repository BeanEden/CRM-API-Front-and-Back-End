from rest_framework.serializers import ModelSerializer, ChoiceField,ReadOnlyField ,SerializerMethodField, DateField, IntegerField
from django.contrib.auth import get_user_model
from epic_event.models.event import Event
User = get_user_model()

def get_support_contact():
    queryset = User.objects.filter(team='support')
    return queryset

class EventDetailSerializer(ModelSerializer):

    support_contact = ChoiceField(choices=get_support_contact(), allow_null=True)
    # attendees = IntegerField(min_value=0, allow_null=True, style={'min_value':0})

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

