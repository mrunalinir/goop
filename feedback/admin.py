from django.contrib import admin

# Register your models here.
from .models import ProductFeedback
from .models import OrderFeedback

@admin.register(ProductFeedback)
class ProdFeedbackModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'rating']

@admin.register(OrderFeedback)
class OrderFeedbackModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'description']
