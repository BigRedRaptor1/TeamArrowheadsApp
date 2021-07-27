from django.contrib import admin
from .models import Ingredient, Inventory, Recipe

admin.site.register(Ingredient)
admin.site.register(Inventory)
admin.site.register(Recipe)
