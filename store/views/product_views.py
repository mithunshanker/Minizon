from django.shortcuts import get_object_or_404, render

from store.models import Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.final_price = round(product.price - (product.price * (product.discount / 100)), 2)
    return render(request, 'product_detail.html', {'product': product, 'page_name': 'Product Detail'})

