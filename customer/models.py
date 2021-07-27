from django.db import models
from django.db.models.fields import IntegerField

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Diners(models.Model):
    mobile_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.mobile_number

class Promotion(models.Model):
    promo_code = models.CharField(max_length=100)
    promo_description = models.CharField(max_length=100, blank=True)
    discount_multiplier = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.promo_code

class Bill(models.Model):
    payment_method = models.CharField(max_length=100, blank=False)
    payment_description = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.payment_method + ': ' + self.payment_description


class OrderModel(models.Model):
    day = models.CharField(max_length=15)
    hour = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now_add=False, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    rating = IntegerField(null=True, blank=False)
    feedback = models.CharField(max_length=100, blank=True)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    mobile_number = models.ForeignKey(Diners, on_delete=models.CASCADE, null=True)
    promo_code = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True)
    payment_method = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=False, default='preparing')


    class Meta:
        db_table = 'ordermodel'

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'




