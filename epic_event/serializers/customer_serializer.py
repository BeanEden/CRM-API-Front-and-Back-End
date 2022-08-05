from rest_framework.serializers import ModelSerializer

from epic_event.models.customer import Customer


class CustomerDetailSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id',
                 'sales_contact',
                 'first_name',
                 'last_name',
                 'email',
                 'phone',
                 'mobile',
                 'company_name'
                  ]