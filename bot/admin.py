from django.contrib import admin

from bot.models import BotUser, Meal, Menu, OrderItem, Order

# Register your models here.

admin.site.register(BotUser)
admin.site.register(Meal)
admin.site.register(Menu)
admin.site.register(OrderItem)
admin.site.register(Order)