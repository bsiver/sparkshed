from django import forms
from dashboard.models import Item
from dashboard.models import Kit
from dashboard.models import KitItem
from dashboard.models import Order

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['item', 'order_quantity']


class KitItemsForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.NumberInput()

    class Meta:
        model = Kit
        fields = '__all__'


KitItemFormset = forms.modelformset_factory(KitItem,
                                            form=KitItemsForm,
                                            extra=1)