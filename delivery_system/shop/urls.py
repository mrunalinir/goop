from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('wholesale/', views.wholesale_product_list, name='wholesale_product_list'),
    path('category/<int:category_id>', views.product_list, name='product_list_by_category'),
    path('category/create', views.category_create, name='create-category'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('product/create', views.product_create, name='create-product'),
    path('product/update/<int:product_id>', views.product_update, name='update-product'),
    path('product/delete/<int:product_id>', views.product_delete, name='delete-product'),
    path('product/my-products/', views.user_products, name='user-products'),
    path('product/products-by-seller/<int:user_id>', views.products_by_seller, name='products-by-seller')
]