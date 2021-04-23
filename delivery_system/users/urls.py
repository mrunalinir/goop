from django.urls import path
from . import views as userviews
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('register/', userviews.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('update-password/', userviews.update_password, name='update-password'),
    path('update-profile/', userviews.updateprofile, name='updateprofile'),
    path('create-address/', userviews.create_address, name='create-address'),
    path('address-edit/<int:addr_id>', userviews.address_details, name='address-edit'),
    path('address-delete/<int:addr_id>', userviews.address_delete, name='address-delete'),
    path('profile/', userviews.profile, name='profile'),
    path('register-as-retailer/', userviews.register_as_retailer, name='register-retailer'),
    path('register-as-wholesaler/', userviews.register_as_wholesaler, name='register-wholesaler'),
    path('wholesaler-requests/', userviews.wholesaler_requests, name='wholesaler-requests'),
    path('wholesaler-request/<int:user_id>', userviews.wholesaler_request_check, name='wholesaler-request-check'),
    path('retailer-requests/', userviews.retailer_requests, name='retailer-requests'),
    path('retailer-request/<int:user_id>', userviews.retailer_request_check, name='retailer-request-check'),
    path('set-address/', userviews.select_address, name='set-address'),
]