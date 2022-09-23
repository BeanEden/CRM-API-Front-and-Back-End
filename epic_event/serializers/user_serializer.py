from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model


User = get_user_model()


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name',
                 'last_name',
                 'email',
                 'password',
                 'team'
                 ]


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                 'first_name',
                 'last_name',
                 'email',
                 'team'
                 ]
