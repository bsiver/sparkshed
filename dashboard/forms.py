from django import forms

from dashboard.models import Item
from dashboard.models import ItemDelivery
from dashboard.models import ItemOrder
from dashboard.models import Kit
from dashboard.models import KitDelivery
from dashboard.models import KitItem
from dashboard.models import KitOrder
import logging
logger = logging.getLogger(__name__)


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

    def clean(self):
        kit = self.cleaned_data.get('kit')
        order_quantity = self.cleaned_data.get('order_quantity')
        for kit_item in kit.get_items_in_kit():
            items_in_stock = kit_item.item.quantity
            items_required = kit_item.quantity * order_quantity
            if items_in_stock < items_required:
                self.add_error('order_quantity', f"Insufficient {kit_item.item.name} in stock to fulfill order "
                               f"({items_in_stock}/{items_required}) in stock")
        return self.cleaned_data


class KitItemForm(forms.ModelForm):

    class Meta:
        model = KitItem
        fields = ['item', 'quantity']


class KitDeliveryForm(forms.ModelForm):

    class Meta:
        model = KitDelivery
        fields = ['kit', 'order']

    def clean(self):

        cleaned_data = super(KitDeliveryForm, self).clean()
        kit = self.cleaned_data['kit']
        order = self.cleaned_data['order']

        for kit_item in kit.get_items_in_kit():
            items_in_stock = kit_item.item.quantity
            items_required = kit_item.quantity * order.order_quantity
            if items_in_stock < items_required:
                self.add_error('kit', f"Insufficient {kit_item.item.name} items in stock to fulfill order "
                               f"({items_in_stock}/{items_required} in stock)")
        return cleaned_data


class ItemDeliveryForm(forms.ModelForm):

    class Meta:
        model = ItemDelivery
        fields = ['item', 'order']