from django.shortcuts import render,get_object_or_404, redirect
from categories.models import Categories
from django.http import HttpResponse
from Cart.models import Cart,CartItem
from .models import Product
from Cart.views import cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from Orders.models import OrderProduct
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
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id(request), product=single_product, is_active=True).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(
        user=request.user,
        product_id=single_product.id).exists()
    else:
        orderproduct = False
    
    reviews = ReviewRating.objects.filter(product_id= single_product.id,status=True)
    context = {
       'single_product':single_product,
       'in_cart':in_cart,
       'orderproduct':orderproduct,
       'reviews':reviews
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

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # Checking if Review Already Exist or not.
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)   #This if for checking if the review exist or not if exist then update it.
            form.save()
            messages.success(request,'Thank you!, Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data= ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
            return redirect(url)
    