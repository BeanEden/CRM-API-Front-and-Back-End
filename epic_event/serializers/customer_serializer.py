"""Customer serializer"""
from rest_framework.serializers import ModelSerializer, ChoiceField
from django.contrib.auth import get_user_model
from epic_event.models.customer import Customer


User = get_user_model()


def get_sales_contact():
    """Get sales user for selection"""
    queryset = User.objects.filter(team='sales')
    return queryset


class CustomerSerializer(ModelSerializer):
    """Customer Serializer"""

    class Meta:
        """Meta class for selecting fields"""
        model = Customer
        fields = ['id',
                  'company_name',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  ]


class AdminCustomerSerializer(ModelSerializer):
    """Admin Customer Serializer"""
    sales_contact = ChoiceField(choices=get_sales_contact(), allow_null=True)

    class Meta:
        """Meta class for selecting fields"""
        model = Customer
        fields = ['id',
                  'sales_contact',
                  'company_name',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'status'
                  ]
