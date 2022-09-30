from django import forms
from dashboard.models import Item
from dashboard.models import ItemOrder
from dashboard.models import Kit
from dashboard.models import KitItem
from dashboard.models import KitOrder


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemOrderForm(forms.ModelForm):

    class Meta:
        model = ItemOrder
        fields = ['item', 'order_quantity']


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = '__all__'


class KitOrderForm(forms.ModelForm):

    class Meta:
        model = KitOrder
        fields = ['kit', 'order_quantity']



class KitItemForm(forms.ModelForm):

    class Meta:
        model = KitItem
        fields = ['item', 'quantity']