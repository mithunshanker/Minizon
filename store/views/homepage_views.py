from django.shortcuts import render
from store.models import Categories, Product
from django.core.paginator import Paginator

def homepage(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q') or ""

    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, is_available=True).order_by('-id')
    elif search_query:
        products = Product.objects.filter(name__icontains=search_query, is_available=True).order_by('-id')
    else:
        products = Product.objects.filter(is_available=True).order_by('-id')

    categories = Categories.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for product in page_obj:
        product.final_price = round(product.price - (product.price * (product.discount / 100)), 2)

    return render(request, 'homepage.html', {
        'products': page_obj,
        'categories': categories,
        'query': search_query,
        'selected_category': category_slug,
        'page_obj': page_obj,
        'page_name': 'Homepage',
    })

