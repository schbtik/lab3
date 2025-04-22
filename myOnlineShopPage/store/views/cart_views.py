from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key)
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart_view')

def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product')
    total = sum(item.get_total_price() for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    cart = get_cart(request)
    if item.cart == cart:
        item.delete()  
    return redirect('cart_view')
