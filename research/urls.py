from django.urls import path
from .views import *

app_name = 'research'

urlpatterns = [
  path('research/', research_view, name='home'), 
  path('research/search/<str:q>/', search_docs, name='search') 
]