from django.urls import path
from store.views import cart_view, home, products_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  
    path('admin/', admin.site.urls),  
    path('cart/', cart_view, name='cart_view'), 
    path('product/', products_view, name='products_view'), 
]

