from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ProductFeedback
from .models import OrderFeedback
from shop.models import Product
from .forms import ProdFeedbackCreateForm
from .forms import OrderFeedbackCreateForm
#from cart.cart import Cart

# Create your views here.

def product_feedback_create(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	if request.method == 'POST':
		form = ProdFeedbackCreateForm(request.POST)
		if form.is_valid():
			#feedback = form.save()
			ProductFeedback.objects.create(product= product, rating = form['rating'].value(), description = form['description'].value())
			return render(request, 'feedback/feedfilled.html', {})
	else:
		form = ProdFeedbackCreateForm()
	return render(request, 'feedback/prodfeedfill.html', {'form': form})

def order_feedback_create(request, order_id):
	order = get_object_or_404(OrderItem, id = order_id)
	if request.method == 'POST':
		form = OrderFeedbackCreateForm(request.POST)
		if form.is_valid():
			#feedback = form.save()
			OrderFeedback.objects.create(order= order, rating = form['rating'].value(), description = form['description'].value())
			return render(request, 'feedback/feedfilled.html', {})
	else:
		form = OrderFeedbackCreateForm()
	return render(request, 'feedback/orderfeedfill.html', {'form': form})

def product_feedback_list(request, product_id):
	products = Product.objects.all()
	feedbacks = ProductFeedback.objects.all()
	context = {'products':products, 'feedbacks': feedbacks}
	if product_id:
		product = Product.objects.get(id=product_id)
		feedbacks = ProductFeedback.objects.filter(product = product)  
		context = {'product':product, 'products':products, 'feedbacks': feedbacks}  
	return render(request, 'feedback/prodfeedbacklist.html', context)

