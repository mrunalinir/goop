#importing template to set up a python filter block in html
from django import template
#importing group as the filters will be based on groups
from django.contrib.auth.models import Group
from order.models import Order

register = template.Library()

@register.filter(name='group')
def group(user, group_name):
    # returns true if the user belongs to a group. Else, false.
    return user.groups.filter(name=group_name).exists()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, status='carted')
        if qs.exists():
            return qs[0].items.count()
    return 0