"""User serializer"""
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta ordering"""
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'password',
                  'team'
                  ]
