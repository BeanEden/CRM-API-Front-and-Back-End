from rest_framework.serializers import ModelSerializer

from epic_event.models.event import Event


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id',
                 'support_contact',
                 'customer_id',
                 'attendees',
                 'event',
                 'notes'
                 ]