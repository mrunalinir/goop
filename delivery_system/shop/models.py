from django.db import models
from users.models import User, Address
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.id])


class Product(models.Model):
    category = models.ManyToManyField('Category', related_name='products', blank=True)
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    stock_units = models.DecimalField(max_digits=5, decimal_places=0, default=32)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField(default='')
    sort = models.CharField(max_length=255)

    class Meta:
        ordering = ['name',]
        
    def __str__(self):
        return self.name+str(self.id)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])
