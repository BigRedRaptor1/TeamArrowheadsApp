from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Diners, Promotion, Bill

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Promotion)
admin.site.register(Diners)
admin.site.register(Bill)
