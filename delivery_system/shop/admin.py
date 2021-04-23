from django.contrib import admin
from .models import Category, Product

#register
admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated', 'seller']
    list_editable = ['price', 'available']
