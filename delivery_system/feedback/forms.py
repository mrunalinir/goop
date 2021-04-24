from django import forms
from .models import ProductFeedback
from .models import OrderFeedback

class ProdFeedbackCreateForm(forms.ModelForm):
	class Meta:
		model = ProductFeedback
		fields = ['rating', 'description']

class OrderFeedbackCreateForm(forms.ModelForm):
    class Meta:
        model = OrderFeedback
        fields = ['rating', 'description']