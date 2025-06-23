from datetime import timedelta
from django.utils import timezone
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Adress, Cart, Cartitem, Order, Order_item


@login_required
def place_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = Cartitem.objects.filter(cart=cart)
    address = Adress.objects.filter(user=user).first()

    if not address:
        return redirect('address_form')

    total = sum(item.subtotal for item in cart_items)

    order = Order.objects.create(
        user=user,
        total_price=total,
        adress=address,
        order_status='Placed'
    )

    for item in cart_items:
        Order_item.objects.create(order=order, product=item.product, quantity=item.quantity)

    cart_items.delete()

    messages.success(request, "✅ Order placed successfully!")
    return redirect('homepage')
@login_required
def checkout_view(request):
    user = request.user

    try:
        address = Adress.objects.get(user=user)
    except Adress.DoesNotExist:
        address = None

    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone = request.POST['phone_number']
        addr = request.POST['adress']
        pincode = request.POST['pincode']

        if address:
            address.full_name = full_name
            address.phone_number = phone
            address.adress = addr
            address.pincode = pincode
            address.save()
        else:
            address = Adress.objects.create(
                user=user,
                full_name=full_name,
                phone_number=phone,
                adress=addr,
                pincode=pincode
            )

        cart = Cart.objects.get(user=user)
        cart_items = Cartitem.objects.filter(cart=cart)

        if not cart_items.exists():
            return redirect('cart_view')

        total = sum(item.subtotal for item in cart_items)

        order = Order.objects.create(
            user=user,
            total_price=total,
            adress=address,
            order_status='Placed',
            placed_at=timezone.now()
        )

        for item in cart_items:
            Order_item.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return render(request, 'order_success.html', {'order': order, 'page_name': 'Order Success'})

    return render(request, 'checkout.html', {'address': address, 'page_name': 'Checkout'})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-placed_at')
    one_day_ago = timezone.now() - timedelta(days=1)

    for order in orders:
        order.can_cancel = order.placed_at >= one_day_ago

    return render(request, 'my_orders.html', {'orders': orders, 'page_name': 'My Orders'})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    one_day_ago = timezone.now() - timedelta(days=1)

    if order.placed_at >= one_day_ago and order.order_status != 'Cancelled':
        order.order_status = 'Cancelled'
        order.save()

        items = Order_item.objects.filter(order=order)
        for item in items:
            item.product.stock += item.quantity
            item.product.save()

        cancelled_orders = Order.objects.filter(user=request.user, order_status='Cancelled').order_by('-placed_at')
        if cancelled_orders.count() > 3:
            for old_order in cancelled_orders[3:]:
                old_order.delete()

    return redirect('my_orders')

