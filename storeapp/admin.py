from django.contrib import admin
from .models import Product,Variation, ReviewRating

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_at','is_available')
    prepopulated_fields= {'slug':('product_name',)}
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','is_active','created_date')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','is_active')
admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)