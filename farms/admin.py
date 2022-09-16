from pyexpat import model
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(FarmProduce)
class FarmProduceAdmin(admin.ModelAdmin):
  list_display = ('name', 'unit_name', 'price_per_unit')


@admin.register(FarmProdudeOrder)
class FarmProduceOrderAdmin(admin.ModelAdmin):
  list_display= ('id', 'produce', 'completed', 'price')