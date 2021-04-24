from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<int:product_id>/prodfeedfill/', views.product_feedback_create, name='prod_feedback_fill'),
    path('<int:order_id>/orderfeedfill/', views.order_feedback_create, name='order_feedback_fill'),
    path('<int:product_id>/prodfeedbacklist/', views.product_feedback_list, name='prod_feedback_list'),

]