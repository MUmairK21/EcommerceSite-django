from django.shortcuts import render,get_object_or_404
from categories.models import Categories
from .models import Product
# Create your views here.
def Store(request,category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Categories,slug=category_slug)
        products = Product.objects.filter(category=category,is_available=True)
        Product_Count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        Product_Count = products.count()
    context = {
        'products': products,
        'count':Product_Count
        }
    return render(request, 'store/store.html',context)

def product_details(request, category_slug, product_slug):
    single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    # here the category__slug will move from product modal to category and then category slug
    context = {
       'single_product':single_product,
    }
    return render(request, 'store/Product_details.html',context)