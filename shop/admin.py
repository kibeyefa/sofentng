from django.contrib import admin
from .models import BillingAddress, Item, OrderItem, Order, Category, ItemImage, Sale, ShopItemReview

# Register your models here.


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'category', 'title', 'price')


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#   pass

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#   list_display = ('id', 'user', 'start_date', 'ordered', 'total_price')

admin.site.register(Category)
# admin.site.register(ItemImage)
# admin.site.register(BillingAddress)
# admin.site.register(ShopItemReview)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'buyer', 'item',
                    'quantity', 'used', 'payment_confirmed', 'completed')
    list_per_page = 20
    list_filter = ['used', 'payment_confirmed', 'completed']
    search_fields = ['id']
