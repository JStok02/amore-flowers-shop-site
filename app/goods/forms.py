from django import forms
from .models import Categories, Products


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'slug', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'slug', 'description', 'price', 'discount', 'category', 'image', 'quantity', 'is_active']