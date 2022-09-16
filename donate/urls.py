from django.urls import path
from .views import *

app_name = 'donate'

urlpatterns = [
  path('donate/', donate_home_view, name='home'),
  path('donate/search/<str:q>/', donate_search_view, name='search'),
  path('donate/detail/<str:pk>/', donate_detail_view, name='detail'),
	path('donate/<str:pk>/delete-all-images/', delete_all_item_images, name=''),
	path('donate/images/<str:pk>/delete/', delete_single_item_image, name=''),
]