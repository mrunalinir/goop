from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('prodfeedfill/<int:product_id>', views.product_feedback_create, name='prod_feedback_fill'),
    path('orderfeedfill/<int:order_id>', views.order_feedback_create, name='order_feedback_fill'),
    path('prodfeedbacklist/<int:product_id>', views.product_feedback_list, name='prod_feedback_list'),

]