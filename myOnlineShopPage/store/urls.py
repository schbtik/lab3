from django.urls import path
from store.views import add_to_cart
from store.views import cart_view
from store.views import home
from store.views import products_view, product_detail, create_order, order_success
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  
    path('admin/', admin.site.urls),
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('product/', products_view, name='products_view'),  
    path('product/<int:product_id>/', product_detail, name='product_detail'),  
    path('order/', create_order, name='create_order'),  
    path('order_success/<int:order_id>/', order_success, name='order_success'),  
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
