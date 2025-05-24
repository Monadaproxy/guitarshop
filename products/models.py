from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.conf import settings
import os

class Product(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=100)
    cat_id = models.IntegerField(default=1)
    author = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)

    def image_filename(self):
        if self.image:
            return os.path.basename(self.image.name)
        return 'No image'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, amount, override_amount = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'amount' : 0, 'price' : str(product.price)}
        if override_amount:
            self.cart[product_id]['amount'] = amount
        else:
            self.cart[product_id]['amount'] += amount
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['amount']
            yield item

    def __len__(self):
        return sum(item['amount'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

    def get_total_price(self):
        total = sum(Decimal(item['price']) * item['amount'] for item in self.cart.values())
        return format(total, '.2f')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return f'{self.product.title} - {self.image}'


