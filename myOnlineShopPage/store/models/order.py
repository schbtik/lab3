# store/models/order.py

from django.db import models
from django.contrib.auth.models import User
from .cart import Cart  # імпортуємо модель Cart
from .product import Product  # імпортуємо модель Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('processing', 'Обробляється'),
        ('completed', 'Завершений'),
        ('cancelled', 'Скасований'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Користувач, який зробив замовлення
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')  # Корзина, пов’язана з замовленням
    order_date = models.DateTimeField(auto_now_add=True)  # Дата та час оформлення замовлення
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Статус замовлення
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Загальна ціна замовлення

    # Дані для оформлення замовлення
    full_name = models.CharField(max_length=255)  # Повне ім’я клієнта
    email = models.EmailField()  # Електронна пошта
    city = models.CharField(max_length=255)  # Місто доставки
    postal_office_number = models.CharField(max_length=10)  # Номер відділення Нової Пошти
    phone_number = models.CharField(max_length=15)  # Номер телефону

    def __str__(self):
        return f'Замовлення #{self.id} від {self.user.username}'

    def calculate_total(self):
        """Розраховує загальну вартість замовлення на основі корзини"""
        return sum(item.get_total_price() for item in self.cart.items.all())
