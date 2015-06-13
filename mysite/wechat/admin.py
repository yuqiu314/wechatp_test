from django.contrib import admin

from .models import Hotel, WechatUser, Order, Bid

# Register your models here.
admin.site.register(Hotel)
admin.site.register(WechatUser)
admin.site.register(Order)
admin.site.register(Bid)