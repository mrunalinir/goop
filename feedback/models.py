from django.db import models
from shop.models import Product
from order.models import OrderItem

# Create your models here.
class ProductFeedback(models.Model):
	product = models.ForeignKey(Product, related_name='feedback_items', on_delete=models.CASCADE) 
	rating = models.PositiveIntegerField()
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.id)

class OrderFeedback(models.Model):
	order = models.ForeignKey(OrderItem, related_name='feedback_orders', on_delete=models.CASCADE)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.id)



