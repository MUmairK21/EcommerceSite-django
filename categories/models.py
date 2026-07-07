from django.db import models
from django.urls import reverse

# Create your models here.
class Categories(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    desc = models.TextField(max_length=255, blank=True)
    Img = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        # this function will brings category products by url
         return reverse('product-by-category', args = [self.slug])
        # this is from preventing default plural name given by admin panel

    def __str__(self):
        return self.category_name
