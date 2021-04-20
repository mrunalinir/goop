from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductFeedback
from .models import OrderFeedback
from .forms import ProdFeedbackCreateForm
from .forms import OrderFeedbackCreateForm
from cart.cart import Cart

# Create your views here.

def product_feedback_create(request):
	#cart = Cart(request)
	if request.method == 'POST':
		form = ProdFeedbackCreateForm(request.POST)
		if form.is_valid():
			feedback = form.save()
			#temp = feedback.product.total_Feedback
			#feedback.product.total_Feedback= temp + 1
			#temp2 = feedback.product.total_rating
			#feedback.product.total_rating = temp2 + feedback.rating
			#for item in cart:
				#ProductFeedback.objects.create(product=item['product'], rating=item['rating'], description=item['description'])
            # clear the cart
			#cart.clear()
			return render(request, 'feedback/prodfeedfilled.html', {'feedback': feedback})
	else:
		form = ProdFeedbackCreateForm()
	return render(request, 'feedback/prodfeedfill.html', {'form': form})

def order_feedback_create(request):
	#cart = Cart(request)
	if request.method == 'POST':
		form = OrderFeedbackCreateForm(request.POST)
		if form.is_valid():
			feedback = form.save()
			#for item in cart:
				#ProductFeedback.objects.create(product=item['product'], rating=item['rating'], description=item['description'])
            # clear the cart
			#cart.clear()
			return render(request, 'feedback/orderfeedfilled.html', {'feedback': feedback})
	else:
		form = OrderFeedbackCreateForm()
	return render(request, 'feedback/orderfeedfill.html', {'form': form})


