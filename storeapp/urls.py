
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Store,name="store"),
    path('category/<slug:category_slug>/',views.Store,name="product-by-category"),
    path('cateory/<slug:category_slug>/<slug:product_slug>',views.product_details,name="product_Details"),
    path('search/',views.search, name='search'),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Configuring Media files URL
