from django.shortcuts import render,get_object_or_404
from categories.models import Categories
from django.http import HttpResponse
from Cart.models import Cart,CartItem
from .models import Product
from Cart.views import cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
def Store(request,category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Categories,slug=category_slug)
        products = Product.objects.filter(category=category,is_available=True)
        Product_Count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page= request.GET.get('page')
        pagedproducts = paginator.get_page(page)
        Product_Count = products.count()
    context = {
        'products': pagedproducts,
        'count':Product_Count
        }
    return render(request, 'store/store.html',context)

def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug) # here the category__slug will move from product modal to category and then category slug
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id(request), product=single_product, is_active=True
).exists()
    except Exception as e:
        raise e
    
    context = {
       'single_product':single_product,
       'in_cart':in_cart
    }
    return render(request, 'store/Product_details.html',context)

def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            Product_Count = products.count()
    context = {
        'products':products,
        'count':Product_Count
    }
    return render(request, 'store/store.html',context)