from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart-add/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('cart-remove/<int:product_id>', views.remove_from_cart, name='remove-from-cart'),
    path('cart-detail/<int:orderitem_id>', views.edit_cart_detail, name='edit-cart-detail'),
    path('checkout-cart/', views.checkout_cart, name='checkout-cart'),
    path('my-orders/', views.my_orders, name='my-orders'),
    path('order-details/<int:order_id>/', views.order_details, name='order-details'),
    path('cancel-order-item/<int:orderitem_id>/', views.cancel_order_item, name='cancel-order-item'),
    path('seller-orders', views.seller_orders, name='seller-orders'),
    path('update-status/<int:orderitem_id>', views.update_status, name='update-status'),
]