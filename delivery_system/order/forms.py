from django import forms
from .models import OrderItem


class CartEditForm(forms.ModelForm):
	class Meta:
		model = OrderItem
		fields = [
		'quantity'
		]


choices = (('online', 'online'), ('offline','offline'))
class CartCheckoutForm(forms.Form):
	mode = forms.MultipleChoiceField(choices = choices, widget=forms.RadioSelect(), label="How would you like to place the order? Online-The items will be delivered to you. Offline-You will have to pick up the items from the seller")
	pickup_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label="What would be a convenient time to pick up/deliver the item?")
