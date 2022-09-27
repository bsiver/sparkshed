from django import forms
from dashboard.models import Item
from dashboard.models import Kit
from dashboard.models import KitItem
from dashboard.models import Order

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['item', 'order_quantity']


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = '__all__'


class KitItemForm(forms.ModelForm):

    class Meta:
        model = KitItem
        fields = ['item', 'quantity']