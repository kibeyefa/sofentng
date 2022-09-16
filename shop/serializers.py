from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Sale, ShopItemReview, User


class ShopItemReviewUserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['username']


class ShopItemreviewSerializer(ModelSerializer):
  sender = StringRelatedField()
  
  class Meta:
    model = ShopItemReview
    fields = ['sender', 'subject', 'review', 'stars']


class SaleSerializer(ModelSerializer):
  class Meta:
    model = Sale
    fields = ['item', 'buyer', 'price', 'id', 'quantity', 'total_price']