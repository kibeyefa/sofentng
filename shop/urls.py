from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path('store/', shop_view, name='store'),
    path('store/search/<str:q>/', product_search_view, name='search'),
    path('store/categories/<str:slug>/', product_category_page, name='category'),
    path('store/detail/<str:slug>/', product_detail_page, name='detail'),
    path('store/detail/<str:slug>/add-review/',
         product_review_add_view, name='detail-review'),
    # path('store/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
    # path('store/<str:slug>/remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    # path('store/<str:slug>/reduce-items-in-cart/', reduce_item_number_in_cart, name='reduce-items-in-cart'),
    # path('store/cart/', cart_view, name='cart'),
    # path('store/cart/checkout/', check_out_view, name='checkout'),
    # path('store/confirm-payment/', confirm_payment_view, name='confirm-payment'),
    path('store/confirm-purchase/<id>/',
         comfirm_purchase, name='confirm-purchase'),
    path('store/<str:pk>/delete-all-images/',
         delete_all_item_images, name=''),
    path('store/images/<str:pk>/delete/',
         delete_single_item_image, name=''),
    #     path('store/orders/complete/<str:pk>/',
    #          mark_order_as_completed, name=''),

    path('store/delete-sale/<id>/', delete_sale),

    path('store/item-reviews/<str:slug>/',
         ShopItemReviewApiView.as_view()),
    path('store/sales/create/', SaleCreateApiView.as_view()),
]
