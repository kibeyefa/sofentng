from django.shortcuts import render, redirect
from django.urls import path
from .views import *

app_name = 'farms'

urlpatterns = [
  path('farms/', farm_home_vew, name="home"),
  path('farms/create-order/', FarmPaymentView.as_view(), name='payment'),
  path('farms/confirm-order/<str:refID>/', farm_payment_confirm, name='confirm-payment'),
]
