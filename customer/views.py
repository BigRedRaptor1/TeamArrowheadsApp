import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import Diners, MenuItem, Category, OrderModel, Promotion, Bill


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        
        temp = MenuItem.objects.all()
        print(appetizers)

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        promo = request.POST.get('promo_code')
        payment_method = request.POST.get('payment_method')
        payment_description = request.POST.get('payment_description')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        print(items)

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            print(menu_item)
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        diner, temp = Diners.objects.get_or_create(mobile_number=mobile_number, name=name)
        bill, temp = Bill.objects.get_or_create(payment_method=payment_method, payment_description=payment_description)
        try:
            promoObject = Promotion.objects.get(promo_code = promo)
        except Promotion.DoesNotExist:
            promoObject, temp = Promotion.objects.get_or_create(promo_code = 'NONE', discount_multiplier = 1)

        price = price*promoObject.discount_multiplier

        order = OrderModel.objects.create(
            price=price,
            mobile_number=diner,
            promo_code=promoObject,
            payment_method=bill
        )
        order.items.add(*item_ids)



        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
