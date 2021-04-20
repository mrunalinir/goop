from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('prodfeedfill/', views.product_feedback_create, name='prod_feedback_fill'),
    path('orderfeedfill/', views.order_feedback_create, name='order_feedback_fill'),
]