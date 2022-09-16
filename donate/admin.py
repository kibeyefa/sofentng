from django.contrib import admin
from .models import *
from django.forms import ClearableFileInput
# Register your models here.
# admin.site.register(DonateItem)

@admin.register(DonateItem)
class DonateItemAdmin(admin.ModelAdmin):
  list_display= ('title', 'donator', 'collector', 'created')
  fields = ('title', 'donator', 'collector' ,'description', ) 

  # @admin.display(empty_value='')
  # def get_images(self, obj):
  #   return obj.images


admin.site.register(DonateItemImage)