from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from store.models import Cart, Cartitem, Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = Cartitem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': 1, 'subtotal': product.price-(product.price*(product.discount/100))}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.subtotal = cart_item.quantity * product.price
        cart_item.save()

    return redirect('cart_view')


# 🛒 View Cart
@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = Cartitem.objects.filter(cart=cart)
    total = sum(item.subtotal for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'page_name': 'Your Cart',
    })


# ❌ Remove from Cart
@login_required
def remove_from_cart(request, item_id):
    Cartitem.objects.filter(id=item_id, cart__user=request.user).delete()
    return redirect('cart_view')


# 🔁 Update Cart
@login_required
def update_cart(request):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        for item in cart.cartitem_set.all():
            quantity = request.POST.get(f'quantities_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.subtotal = item.quantity * float(item.product.price - (item.product.price * item.product.discount / 100))
                item.save()
    return redirect('cart_view')
