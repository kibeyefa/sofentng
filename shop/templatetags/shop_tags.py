from django import template
register = template.Library()
from shop.models import *

@register.simple_tag(name='add_or_remove')
def add_or_remove(cart, user, item):
  if user.is_authenticated:
    try:
      order_item = OrderItem.objects.get(user=user, ordered=False, item=item)
      if order_item in cart.items.all():
        return "Remove from cart" 
    except Exception as e:
      print(e)
      return 'Add to cart' 

  return 'Add to cart'


@register.simple_tag(name='add_or_remove_url')
def add_or_remove_url(cart, user, item):
  if user.is_authenticated:
    try:
      order_item = OrderItem.objects.get(user=user, ordered=False, item=item)
      if order_item in cart.items.all():
        return f'/store/{item.slug}/remove-from-cart/' 
    except Exception as e:
      print(e)
      return f'/store/{item.slug}/add-to-cart/'

  return f'/store/{item.slug}/add-to-cart/'

