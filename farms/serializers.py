from rest_framework.serializers import ModelSerializer
from .models import FarmProdudeOrder


class FarmProduceOrderSerialzer(ModelSerializer):
  class Meta:
    model = FarmProdudeOrder
    fields = ['id', 'produce', 'unit', 'first_name', 'last_name', 'email', 'address', 'phone_no']