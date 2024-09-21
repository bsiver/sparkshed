from django import forms
from django.forms import inlineformset_factory

from sparkshed.models import Item
from sparkshed.models import ItemDelivery
from sparkshed.models import ItemOrder
from sparkshed.models import Kit
from sparkshed.models import KitDelivery
from sparkshed.models import KitItem
from sparkshed.models import KitOrder
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
        fields = ['name']


class KitItemForm(forms.ModelForm):
    class Meta:
        model = KitItem
        fields = ['item', 'quantity']


KitItemFormSet = inlineformset_factory(
    Kit, KitItem, form=KitItemForm,
    fields=['item', 'quantity'], extra=1, can_delete=False)


class KitOrderForm(forms.ModelForm):
    class Meta:
        model = KitOrder
        fields = ['kit', 'order_quantity', 'recipient']

    def clean(self):
        super(KitOrderForm, self).clean()
        order = self.instance
        kit = order.kit
        order_quantity = order.order_quantity

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