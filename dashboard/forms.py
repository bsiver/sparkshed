from django import forms
from dashboard.models import Item
from dashboard.models import Order


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'order_quantity']
