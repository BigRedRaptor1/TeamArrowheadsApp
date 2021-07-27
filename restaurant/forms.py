from django import forms
from .models import Inventory, Recipe


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ('ingredient', 'quantity', 'last_updated')
        labels = {
            'ingredient':'Ingredient',
            'quantity':'Quantity',
            'last_updated':'Last Updated'
            
        }

    def __init__(self, *args, **kwargs):
        super(InventoryForm,self).__init__(*args, **kwargs)

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('menu_item', 'ingredient', 'quantity')
        labels = {
            'menu_item':'Menu Item',
            'ingredient':'Ingredient',
            'quantity':'Quantity',
            
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm,self).__init__(*args, **kwargs)