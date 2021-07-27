from django.db import models
from customer.models import MenuItem

# Create your models here.

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=100)
    ingredient_description = models.CharField(max_length=100)
    recipe_quantity = models.ManyToManyField('customer.MenuItem', through='Recipe')

    def __str__(self):
        return self.ingredient

class Inventory(models.Model):
    last_updated = models.CharField(max_length=100)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    quantity= models.CharField(max_length=15)

    def __str__(self):
        return self.ingredient.ingredient + " Inventory"

class Recipe(models.Model):
    menu_item = models.ForeignKey('customer.MenuItem', blank=True, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', blank=True, on_delete=models.CASCADE)
    quantity = models.FloatField()
  
    class Meta:
        unique_together = ['menu_item', 'ingredient']
