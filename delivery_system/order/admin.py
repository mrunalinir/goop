from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['id']

admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    inlines = [OrderItemInline]