from django import forms
#The model for which we are creating form
from users.models import User, Address
from .models import Product, Category

class CreateCategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']

class CreateProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'category', 'name', 'image', 'description', 'price', 'original_price', 'available', 'stock_units'
		]

class UpdateProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'category', 'name', 'image', 'description', 'price', 'original_price', 'available', 'stock_units', 
		]