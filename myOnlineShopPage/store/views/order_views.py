from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, CartItem, Order

@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()

    if not cart or cart.items.count() == 0:
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        postal_office_number = request.POST.get('postal_office_number')

        total_price = sum(item.get_total_price() for item in cart.items.all())

        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_price=total_price,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            city=city,
            postal_office_number=postal_office_number,
            status='pending'
        )

        cart.is_active = False
        cart.save()

        return redirect('order_success', order_id=order.id)

    return render(request, 'store/order.html', {
        'items': cart.items.select_related('product'),
        'total': sum(item.get_total_price() for item in cart.items.all())
    })



def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/home.html', {'order': order})
