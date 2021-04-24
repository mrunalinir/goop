from django.db import models
from django.urls import reverse
from shop.models import Product
from order.models import OrderItem
from users.models import User

# Create your models here.
class ProductFeedback(models.Model):
	product = models.ForeignKey(Product, related_name='feedback_items', on_delete=models.CASCADE) 
	rating = models.PositiveIntegerField(default=5)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.id)

	def get_avg_rating(self, product_id):
		product = get_object_or_404(Product, id=product_id)
		feedback = ProductFeedback.objects.all()
		total_rating = 0
		total_prod = 0
		for each in feedback:
			if (each.product == product):
				total_rating = total_rating + each.rating
				total_prod = total_prod + 1
		av_rating = total_rating/total_prod
		return av_rating


class OrderFeedback(models.Model):
	order = models.ForeignKey(OrderItem, related_name='feedback_orders', on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
	rating = models.PositiveIntegerField(default=5)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.id)



