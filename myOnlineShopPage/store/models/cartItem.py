from django.db import models
from django.contrib.auth.models import User
from .product import Product
from .cart import Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.product.price * self.quantity
