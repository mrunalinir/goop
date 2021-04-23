from django.shortcuts import render, get_object_or_404, redirect
# from cart.cart import Cart
from django.utils import timezone
from django.contrib import messages
from .models import OrderItem, Order
from shop.models import Product
from users.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group
from .forms import CartEditForm, CartCheckoutForm


def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, str):
            groups =(group, )
        else:
            groups = group
        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)


def refresh_order(order):
    count = 0
    closed = 0
    for item in order.items.all():
        count+=1
        if item.closed == True:
            closed+=1
    if closed==count:
        order.closed = True
        order.status = "completed"
        order.save()    

@login_required
def cart(request):
    user = request.user
    order_qs = Order.objects.filter(user=request.user, status='carted')
    if order_qs.exists():
        cart = order_qs[0]
    else:
        cart = []
    context={'cart':cart}
    return render(request, 'order/cart-detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_item, created = OrderItem.objects.get_or_create(
        item=product,
        user=request.user,
        status="carted"
    )
    order_qs = Order.objects.filter(user=request.user, status='carted')
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item=product).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order:cart")
    else:
        created = timezone.now()
        order = Order.objects.create(
            user=request.user, created=created)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order:cart")


@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(
        user=request.user,
        status="carted"
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item=item).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                status='carted'
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order:cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order:cart")


@login_required
def edit_cart_detail(request, orderitem_id):
    orderitem = get_object_or_404(OrderItem, id=orderitem_id)
    form = CartEditForm(request.POST or None, instance=orderitem)
    if form.is_valid():
        form.save()
        return redirect('order:cart')
    context={'form':form, 'orderitem':orderitem}
    return render(request, 'order/cart-edit.html', context)


@login_required
def checkout_cart(request):
    user = request.user
    if user.location==None:
        messages.info(request, "You need to have a valid location saved to place an order")
        return redirect("users:set-address")
    order_qs = Order.objects.filter(user=user, status="carted")
    if order_qs.exists():
        order = order_qs[0]
        if not order.items.all:
            messages.info(request, "You currently do not have any items in your cart")
            return redirect("order:cart")
        for item in order.items.all():
            if(item.quantity > item.item.stock_units):
                messages.info(request, "An item in your cart does not have enough stock units available to satisfy your request")
                return redirect("order:cart")

        if request.POST:
            order.mode = request.POST.get('mode')
            order.status = "ordered"
            order.created = timezone.now()
            if order.mode=='offline':
                order.deliver_by = request.POST.get('date')
            order.address = user.location
            order.save()
            for item in order.items.all():
                item.mode = order.mode
                item.status = order.status
                item.created = order.created
                item.deliver_by = order.deliver_by
                item.address = order.address
                item.item.stock_units -= item.quantity
                item.save()
                return redirect("shop:product_list")
        context = {'order':order}
        return render(request, 'order/checkout_cart.html', context)
    else:
        messages.info(request, "You currently do not have a valid cart")
        return redirect("order:cart")

@login_required
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user = user, status='ordered')
    for order in orders:
        refresh_order(order)
    context = {'orders':orders}
    return render(request, 'order/my-orders.html', context)

@login_required
def order_details(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    refresh_order(order)

    context = {'order':order}
    return render(request, 'order/order-details.html', context)

@login_required
def cancel_order_item(request, orderitem_id):
    item = get_object_or_404(OrderItem, id=orderitem_id)
    if request.POST:
        if item.closed == False:
            item.status = "cancelled"
            item.closed = True
            if request.POST.get("comments"):
                item.comments = request.POST.get("comments")
            item.save()
        else:
            messages.info(request, "You cannot cancel an order that is closed")
        return redirect("order:my-orders")
    context = {'item':item}
    return render(request, 'order/cancel-order-item.html', context)

@group_required('merchant')
def seller_orders(request):
    user = request.user
    items = OrderItem.objects.filter(seller=user)
    context = {'items':items}
    return render(request, 'order/seller-orders.html', context)

@group_required('merchant')
def update_status(request, orderitem_id):
    item = get_object_or_404(OrderItem, id=orderitem_id)
    if request.POST:
        item.status = request.POST.get("status")
        if item.status == 'in_transit':
            item.deliver_by = request.POST.get('deliver_by')
        if item.status == 'delivered' or item.status == 'cancelled':
            item.closed = True
        if request.POST.get('comments'):
            item.comments = request.POST.get("comments")
        item.save()
        return redirect("order:seller-orders") 

    context = {'item':item}
    return render(request, 'order/update_status.html', context)


