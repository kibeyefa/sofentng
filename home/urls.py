from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
]