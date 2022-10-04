from rest_framework.serializers import ModelSerializer, ChoiceField, SerializerMethodField
from django.contrib.auth import get_user_model
from epic_event.models.event import Event
User = get_user_model()

class EventDetailSerializer(ModelSerializer):

    # support_contact = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id',
                 'support_contact',
                 'customer_id',
                 'contract_id',
                 'attendees',
                 'event',
                 'notes'
                 ]