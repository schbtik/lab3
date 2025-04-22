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
