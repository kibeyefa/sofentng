from os import fdopen
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('accounts/check-email/<str:email>/',
         EmailConfirmView.as_view(), name='contact'),

    path('accounts/make-user-admin/', make_user_admin),

    path('accounts/contact/', contact, name='contact'),
    path('accounts/admin/messages/', admin_messages_view, name='admin-messages'),
    path('accounts/admin/messages/respond/',
         admin_messages_respond_view, name='admin-messages-respond'),

    path('accounts/notifications/',
         account_notifications_view, name='notification'),
    path('accounts/notifications/search/<str:q>/',
         account_notifications_search_view, name='notification-search'),

    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/dashboard/', dashboard_view, name='dashboard'),
    path('accounts/self/delete/', self_delete_account_view,
         name='self_account_delete'),
    path('accounts/e-commerce/orders/', self_orders_view, name='self-orders'),
    path('accounts/e-commerce/store/', self_store_view, name='self-store'),
    path('accounts/e-commerce/store/add/',
         self_store_add_view, name='self-store-add'),
    path('accounts/e-commerce/store/<slug>/',
         admin_self_store_single_store_item, name='self-store-single'),
    path('accounts/e-commerce/store/<slug>/chat/<username>/',
         admin_self_store_single_store_item_chat, name='self-store-single-chat'),
    path('accounts/e-commerce/store/<slug>/make-sale/<username>/',
         make_sale, name='make-sale'),
    path('accounts/e-commerce/edit-item/<str:pk>/',
         self_store_edit_view, name='self-store-edit'),


    path('accounts/donate/items/', self_donate_view, name='self-donate-items'),
    path('accounts/donate/edit-item/<str:pk>/',
         self_donate_edit_view, name='self-donate-edit'),
    path('accounts/donate/items/add/',
         self_donate_item_add_view, name='self-donate-add'),


    path('accounts/admin/orders/', admin_order_view, name='admin-orders'),
    path('accounts/admin/orders/search/<str:q>/',
         admin_order_search_view, name='admin-orders-search'),
    path('accounts/admin/items/', admin_items_view, name='admin-items'),
    path('accounts/admin/items/<slug>/',
         admin_single_store_item, name='admin-single-item'),
    path('accounts/admin/items/<slug>/chat/<id>/',
         admin_item_chat, name='admin-single-item-chat'),
    path('accounts/admin/items/search/<str:q>/',
         admin_items_search_view, name='admin-items-search'),

    path('accounts/admin/sales/<id>/mark-complete/', complete_sale),

    path('accounts/admin/donate-items/',
         admin_donate_items_view, name='admin-donate-items'),
    path('accounts/admin/donate-items/search/<str:q>/',
         admin_donate_items_search_view, name='admin-donate-items-search'),

    path('accounts/admin/research/', admin_research_view, name='admin-research'),
    path('accounts/admin/research/add/',
         add_document_view, name='admin-research-add'),
    path('accounts/admin/research/<str:pk>/delete/',
         delete_document_view, name='admin-research-delete'),
    path('accounts/admin/research/search/<str:q>/',
         admin_research_search_view, name='admin-research-search'),

    path('accounts/admin/farms/items/', farm_items_view, name='admin-farm-items'),
    path('accounts/admin/farms/items/<str:pk>/change-availability/',
         farm_items_edit_view, name='farms-change-availability'),
    path('accounts/admin/farms/items/<str:pk>/delete/',
         farm_items_delete_view, name='farms-items-delete'),
    path('accounts/admin/farms/orders/',
         farm_orders_view, name='admin-farm-orders'),
    path('accounts/admin/farms/orders/search/<str:q>/',
         farm_orders_search_view, name='admin-farm-order-search'),

    path('accounts/admin/users/', admin_user_view, name='users'),

    path('accounts/add-account-number/', AccountNumberCreateView.as_view()),
    path('accounts/verify-account-number/', VerifyAccountNumberView.as_view()),

    path('404/', error_404_page, name='404')
]
