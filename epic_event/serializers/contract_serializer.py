from rest_framework.serializers import ModelSerializer, ChoiceField, DateField, CharField
from django.contrib.auth import get_user_model
from epic_event.models.contract import Contract

User = get_user_model()

def get_sales_contact():
    queryset = User.objects.filter(team='sales')
    return queryset

class ContractDetailSerializer(ModelSerializer):

    sales_contact = ChoiceField(choices=get_sales_contact(), allow_null=True)

    class Meta:
        model = Contract
        fields = ['id',
                 'sales_contact',
                 'customer_id',
                 'name',
                 'status',
                 'amount',
                 'payment_due'
                  ]
        extra_kwargs = {
            'status': {'read_only': True},
        }


class ContractManagementSerializer(ModelSerializer):

    sales_contact = ChoiceField(choices=get_sales_contact(), allow_null=True)

    class Meta:
        model = Contract
        fields = ['id',
                 'sales_contact',
                 'customer_id',
                 'name',
                 'status',
                 'amount',
                 'payment_due'
                  ]
        extra_kwargs = {
            'status': {'read_only': True},
        }