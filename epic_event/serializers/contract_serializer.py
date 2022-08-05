from rest_framework.serializers import ModelSerializer

from epic_event.models.contract import Contract


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id',
                 'sales_contact',
                 'customer_id',
                 'status',
                 'amount',
                 'payment_due'
                  ]