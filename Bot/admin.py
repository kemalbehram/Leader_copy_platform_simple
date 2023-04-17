from django.contrib import admin

from Bot.models import Admin, Traders, Signal, Users


@admin.register(Admin)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_id', ]


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_id', ]


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ['name_trader', 'symbol', 'side']


@admin.register(Traders)
class TradersAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']


# @admin.register(UserFollowing)
# class TradersAdmin(admin.ModelAdmin):
#     list_display = ['trader_f', 'user_f']
