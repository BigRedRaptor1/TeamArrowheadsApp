from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from django.db.models import Q
from django.db.models import Count, Avg
from datetime import date
import calendar
from customer.models import MenuItem, OrderModel
from .forms import InventoryForm, RecipeForm
from .models import Inventory, Recipe

class AllOrders(View):
    def get(self, request, *args, **kwargs):
        orders = OrderModel.objects.all()

        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard1.html', context)
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        print(today.weekday())
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price
            if order.status == 'preparing':
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)

class Advanced(View):
    def get(self, request, *args, **kwargs):

        orders1 = OrderModel.objects.values('day').annotate(avg_rating = Avg('rating'), count = Count("id")).order_by('-count')
        orders2 = OrderModel.objects.values('hour').annotate(avg_rating = Avg('rating'), count = Count("id")).order_by('-count')


        dict = {}
        temp = {}

        bad = OrderModel.objects.raw('SELECT * FROM ordermodel WHERE rating <=3')

        for i in bad:
            for r in i.items.all():
                dict[r] = dict.get(r, 0)+1

        temp = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        for i in temp:
            print(i[0])
            print(i[1])

        # pass total number of orders and total revenue into template
        context = {
            'days': orders1,
            'hours': orders2,
            'poor': temp
        }

        return render(request, 'restaurant/output1.html', context)

class OrderDetails(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        print(order)
        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        today = datetime.today()
        now = timezone.now()
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        order = OrderModel.objects.get(pk=pk)
        order.status='completed'
        order.completed_at = datetime.now()
        order.rating = rating
        order.feedback = feedback
        order.day = calendar.day_name[today.weekday()]
        order.hour = now.hour
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

def inventory_list(request):
    context = {'inventory_list': Inventory.objects.all()}
    return render(request, "restaurant/inventory_list.html", context)


def inventory_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = InventoryForm()
        else:
            inventory = Inventory.objects.get(pk=id)
            form = InventoryForm(instance=inventory)
        return render(request, "restaurant/inventory_form.html", {'form': form})
    else:
        if id == 0:
            form = InventoryForm(request.POST)
        else:
            inventory = Inventory.objects.get(pk=id)
            form = InventoryForm(request.POST,instance= inventory)
        if form.is_valid():
            form.save()
        return redirect('/restaurant/inventory-list')


def inventory_delete(request,id):
    inventory = Inventory.objects.get(pk=id)
    inventory.delete()
    return redirect('/restaurant/inventory-list')


def recipe_list(request):
    context = {'recipe_list': Recipe.objects.all()}
    return render(request, "restaurant/recipe_list.html", context)


def recipe_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = RecipeForm()
        else:
            recipe = Recipe.objects.get(pk=id)
            form = RecipeForm(instance=recipe)
        return render(request, "restaurant/recipe_form.html", {'form': form})
    else:
        if id == 0:
            form = RecipeForm(request.POST)
        else:
            recipe = Recipe.objects.get(pk=id)
            form = RecipeForm(request.POST,instance= recipe)
        if form.is_valid():
            form.save()
        return redirect('/restaurant/recipe-list')


def recipe_delete(request,id):
    recipe = Recipe.objects.get(pk=id)
    recipe.delete()
    return redirect('/restaurant/recipe-list')

