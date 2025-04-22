from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem, Order

class StoreModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.category = Category.objects.create(name='Цукерки')
        self.product = Product.objects.create(
            category=self.category,
            name='Шоколадні трюфелі',
            description='Смачні трюфелі з чорного шоколаду',
            price=150.00,
            weight='200г',
            brand='SweetLife'
        )

        self.cart = Cart.objects.create(user=self.user)

    def test_add_product_to_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(cart_item.get_total_price(), 300.00)

    def test_cart_total_price(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        total = self.cart.get_total_price()
        self.assertEqual(total, 450.00)

    def test_order_creation_and_total(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        order = Order.objects.create(
            user=self.user,
            cart=self.cart,
            total_price=self.cart.get_total_price(),
            full_name='Олена Петрова',
            email='olena@example.com',
            city='Львів',
            postal_office_number='5',
            phone_number='0987654321'
        )
        self.assertEqual(order.total_price, 150.00)
        self.assertEqual(order.calculate_total(), 150.00)
        self.assertEqual(order.status, 'pending')

    def test_string_representations(self):
        self.assertEqual(str(self.product), 'Шоколадні трюфелі')
        self.assertEqual(str(self.category), 'Цукерки')
        self.assertEqual(str(self.cart), f'Кошик #{self.cart.id}')

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Category, Cart, CartItem

class StoreViewsTestCase(TestCase):
    def setUp(self):
        # Створення користувача та категорії для тестів
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Солодощі')
        self.product = Product.objects.create(
            category=self.category,
            name='Цукерки',
            description='Смачні цукерки',
            price=50.00,
            weight='200г',
            brand='CandyCo'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass')  # Логінімося для тестів


    def test_cart_view(self):
        """Тестуємо відображення кошика"""
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кошик')

    def test_add_to_cart(self):
        """Тестуємо додавання товару до кошика"""
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart_view'))
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart(self):
        """Тестуємо видалення товару з кошика"""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.post(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertRedirects(response, reverse('cart_view'))
        self.assertEqual(CartItem.objects.count(), 0)

    def test_create_order_view(self):
        """Тестуємо створення замовлення"""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.post(reverse('create_order'), {
            'full_name': 'Іван Іванов',
            'email': 'ivan@example.com',
            'phone_number': '1234567890',
            'city': 'Київ',
            'postal_office_number': '12',
        })
        self.assertRedirects(response, reverse('order_success', args=[1]))  # Передбачається, що замовлення створиться з id = 1


    def test_products_view(self):
        """Тестуємо сторінку товарів з фільтрами"""
        response = self.client.get(reverse('products_view') + '?category=Солодощі&min_price=30&max_price=100')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Солодощі')
        self.assertContains(response, 'Цукерки')

    def test_product_detail_view(self):
        """Тестуємо сторінку детальної інформації про товар"""
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Цукерки')
        self.assertContains(response, 'Смачні цукерки')
