from rest_framework.serializers import ModelSerializer, SerializerMethodField

from epic_event.models.customer import Customer


class CustomerDetailSerializer(ModelSerializer):
    # sales_contact = SerializerMethodField('_is_my_find')
    #
    # def get_sales_contact(self, sales_contact_id):
    #     return setattr(sales_contact_id, 'sales_contact', "")
    #
    # def _is_my_find(self, obj):
    #     user_id = self.context.get("user_id")
    #     if user_id:
    #         return user_id in obj.my_objects.values_list("user_id", flat=True)
    #     return False

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