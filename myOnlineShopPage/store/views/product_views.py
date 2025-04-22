
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category


def products_view(request):
    products = Product.objects.all() 
    return render(request, 'store/products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def products_view(request):
    category_name = request.GET.get('category')  
    min_price = request.GET.get('min_price')  
    max_price = request.GET.get('max_price') 
    brand = request.GET.getlist('brand')  
    search_query = request.GET.get('search')  


    if min_price == "None":
        min_price = None
    if max_price == "None":
        max_price = None

    products = Product.objects.all()
    if category_name:
        products = products.filter(category__name=category_name)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if brand:
        products = products.filter(brand__in=brand)


    if search_query:
        products = products.filter(name__icontains=search_query)


    categories = Category.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()


    grouped_products = {}
    for product in products:
        if product.category.name not in grouped_products:
            grouped_products[product.category.name] = []
        grouped_products[product.category.name].append(product)

    return render(request, 'store/products.html', {
        'grouped_products': grouped_products,  
        'categories': categories,
        'brands': brands,
        'selected_category': category_name,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'selected_brands': brand,
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
   
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })