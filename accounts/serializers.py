from pyexpat import model
from rest_framework.serializers import ModelSerializer
from allauth.account.models import EmailAddress
from .models import UserAccountNumber


class EmailAddressSerializer(ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ['email']


class AccountCreationSerializer(ModelSerializer):
    class Meta:
        model = UserAccountNumber
        fields = '__all__'
