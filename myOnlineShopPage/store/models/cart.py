from django.db import models
from django.contrib.auth.models import User
from .product import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Кошик #{self.id}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

