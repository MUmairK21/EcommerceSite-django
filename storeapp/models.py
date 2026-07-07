from django.db import models
from categories.models import Categories
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    Images = models.ImageField(upload_to='photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_Details', args=[self.category.slug, self.slug])