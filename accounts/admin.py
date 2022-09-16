from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'admin')


@admin.register(AvailableBanks)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'active', 'type')
    list_max_show_all = 20
    list_display_links = ('id', 'name')
    # list_filter = ('name')


@admin.register(UserAccountNumber)
class AccountNumberAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank', 'account_number', 'account_name')
    list_display_links = None


admin.site.register(Message)
