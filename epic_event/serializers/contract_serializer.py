"""Contract serializer"""
from rest_framework.serializers import ModelSerializer, ChoiceField
from django.contrib.auth import get_user_model
from epic_event.models.contract import Contract


User = get_user_model()


def get_sales_contact():
    """Get sales user for selection"""
    queryset = User.objects.filter(team='sales')
    return queryset


class ContractSerializer(ModelSerializer):
    """Contract serializer"""

    class Meta:
        """Meta class for selecting fields"""
        model = Contract
        fields = ['id',
                  'name',
                  'status',
                  'amount',
                  'payment_due',
                  ]


class AdminContractSerializer(ModelSerializer):
    """Contract serializer for the management"""
    sales_contact = ChoiceField(choices=get_sales_contact(), allow_null=True)

    class Meta:
        """Meta class for selecting fields"""
        model = Contract
        fields = ['id',
                  'sales_contact',
                  'customer_id',
                  'name',
                  'status',
                  'amount',
                  'payment_due'
                  ]
