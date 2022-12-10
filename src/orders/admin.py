from django.contrib import admin
from orders.models import Order, OrderItem, PromoCode
# Register your models here.

admin.site.register([Order,OrderItem,PromoCode])