from django.db import models
from shop.models import Product
from users.models import User
from django.urls import reverse

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=255, default='carted')
    comments = models.CharField(max_length=511, blank=True, null=True)
    mode = models.CharField(max_length=255, blank=True, null=True)
    deliver_by = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def total_cost(self):
        return self.quantity * self.item.price

    def seller(self):
        return self.item.seller


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, related_name='orders')
    status = models.CharField(max_length=255, default='carted')
    comments = models.CharField(max_length=511, blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(blank = True, null = True)
    mode = models.CharField(max_length=255, blank=True, null=True)
    deliver_by = models.DateTimeField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user}'s {self.id} Order"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_cost()
        return total





