import json
import logging
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ItemDeliveryForm
from .forms import ItemForm
from .forms import ItemOrderForm
from .forms import KitDeliveryForm
from .forms import KitForm
from .forms import KitItemForm
from .forms import KitItemFormSet
from .forms import KitOrderForm
from .models import Item
from .models import ItemDelivery
from .models import ItemOrder
from .models import Kit
from .models import KitDelivery
from .models import KitItem
from .models import KitOrder

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def index(request):
    items = Item.objects.with_quantities_and_kits()
    kit_orders = KitOrder.objects.all()
    item_orders = ItemOrder.objects.all()
    context = {
        'order': kit_orders.union(item_orders),
        'items': items,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def products(request):
    items = Item.objects.with_quantities_and_kits()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            item_name = form.cleaned_data.get('name')
            messages.success(request, f'{item_name} has been added')
            return redirect('sparkshed-items')
    else:
        form = ItemForm()
    context = {
        'items': items,
        'form': form
    }
    return render(request, 'dashboard/items.html', context)


@login_required(login_url='user-login')
def item_detail(request, pk):
    context = {

    }
    return render(request, 'dashboard/items_detail.html', context)


@login_required(login_url='user-login')
def customers(request):
    customer = User.objects.all()
    context = {
        'customer': customer,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
def customer_detail(request, pk):
    customers = User.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required(login_url='user-login')
def item_edit(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sparkshed-items')
    else:
        form = ItemForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/items_edit.html', context)


@login_required(login_url='user-login')
def item_delete(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('sparkshed-items')
    context = {
        'item': item
    }
    return render(request, 'dashboard/items_delete.html', context)


@login_required(login_url='user-login')
def order(request):
    kit_orders = list(KitOrder.objects.all())
    item_orders = list(ItemOrder.objects.all())

    kit_form = KitOrderForm()
    item_form = ItemOrderForm()

    context = {
        'item_form': item_form,
        'kit_form': kit_form,
        'new_kit_order_url': reverse('kit-order-create'),
        'new_item_order_url': reverse('item-order-create'),
        'item_orders': item_orders,
        'kit_orders': kit_orders
    }
    return render(request, 'dashboard/order.html', context)


@login_required(login_url='user-login')
def kit_order(request):
    return _create_order(request, 'kit')


@login_required(login_url='user-login')
def item_order(request):
    return _create_order(request, 'item')


def _create_order(request, order_type):
    if order_type == 'item':
        form = ItemOrderForm(request.POST)
    elif order_type == 'kit':
        form = KitOrderForm(request.POST)
    else:
        raise Http404()
    if form.is_valid():
        obj = form.save(commit=False)
        obj.customer = request.user
        obj.save()

    kit_orders = list(KitOrder.objects.all())
    item_orders = list(ItemOrder.objects.all())

    item_form = ItemOrderForm()

    context = {
        'item_form': item_form,
        'kit_form': form,
        'new_kit_order_url': reverse('kit-order-create'),
        'new_item_order_url': reverse('item-order-create'),
        'item_orders': item_orders,
        'kit_orders': kit_orders
    }

    return render(request, 'dashboard/order.html', context)


@login_required(login_url='user-login')
def order_edit(request, type, pk):
    if type == 'kit':
        order = get_object_or_404(KitOrder, id=pk)
        form = KitOrderForm({'order_quantity': order.order_quantity}, instance=order)
    elif type == 'item':
        order = ItemOrder.objects.get(id=pk)
        form = ItemOrderForm(request.POST, instance=order)
    else:
        return Http404()
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('sparkshed-order')
    context = {
        'form': form
    }
    return render(request, 'dashboard/order_edit.html', context)


@login_required(login_url='user-login')
def order_delete(request, type, pk):
    if type == 'kit':
        order = KitOrder.objects.get(id=pk)
    elif type == 'item':
        order = ItemOrder.objects.get(id=pk)
    else:
        return Http404()
    if request.method == 'POST':
        order.delete()
        return redirect('sparkshed-order')
    context = {
        'order': order
    }
    return render(request, 'dashboard/order_delete.html', context)


@login_required()
def kit(request):
    kit_items = KitItem.objects.all()
    context = {
        'kit_items': kit_items
    }
    return render(request, "dashboard/kits.html", context)


@login_required
def create_or_edit_kit(request, id=None):
    if id:
        kit = get_object_or_404(Kit, id=id)
    else:
        kit = None

    if request.method == 'POST':
        kit_form = KitForm(request.POST, instance=kit)
        kit_item_formset = KitItemFormSet(request.POST, instance=kit)

        if kit_form.is_valid() and kit_item_formset.is_valid():
            kit = kit_form.save()
            item_quantities = defaultdict(int)

            for form in kit_item_formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:
                        form.instance.delete()
                    continue

                item = form.cleaned_data.get('item')
                quantity = form.cleaned_data.get('quantity', 0)
                if item:
                    item_quantities[item] += quantity

            for item, total_quantity in item_quantities.items():
                if total_quantity == 0:
                    KitItem.objects.filter(kit=kit, item=item).delete()
                else:
                    KitItem.objects.update_or_create(
                        kit=kit, item=item,
                        defaults={'quantity': total_quantity}
                    )

            return redirect('kits')
    else:
        kit_form = KitForm(instance=kit)
        kit_item_formset = KitItemFormSet(instance=kit)

    return render(request, 'dashboard/kit_create.html', {
        'kit_form': kit_form,
        'kit_item_formset': kit_item_formset,
    })

@login_required(login_url='user-login')
def kit_delete(request, id):
    kit = Kit.objects.get(id=id)
    if request.method == 'POST':
        kit.delete()
        return redirect('kits')
    context = {
        'kit': kit
    }
    return render(request, 'dashboard/kit_delete.html', context)


@login_required(login_url='user-login')
def delivery(request):
    kit_deliveries = list(KitDelivery.objects.all())
    item_deliveries = list(ItemDelivery.objects.all())

    kit_form = KitDeliveryForm()
    item_form = ItemDeliveryForm()

    context = {
        'item_form': item_form,
        'kit_form': kit_form,
        'item_deliveries': item_deliveries,
        'kit_deliveries': kit_deliveries
    }
    return render(request, 'dashboard/delivery.html', context)


@login_required(login_url='user-login')
def create_delivery(request, type, order_id):
    if type == 'item':
        order = get_object_or_404(ItemOrder, id=order_id)
        delivery = ItemDelivery(item=order.item, order=order)
        form = ItemDeliveryForm(instance=delivery)
    elif type == 'kit':
        order = get_object_or_404(KitOrder, id=order_id)
        delivery = KitDelivery(kit=order.kit, order=order)
        form = KitDeliveryForm({'kit': order.kit, 'order': order}, instance=delivery)
    else:
        raise Http404()

    obj = form.save(commit=False)
    obj.customer = request.user
    obj.clean()
    obj.save()

    context = {
        'form': form
    }

    return render(request, 'dashboard/delivery.html', context)




@login_required(login_url='user-login')
def delivery_edit(request, type, pk):
    if type == 'kit':
        delivery = get_object_or_404(KitDelivery, id=pk)
        form = KitDeliveryForm({'kit': delivery.kit, 'order': delivery.order}, instance=delivery)
    elif type == 'item':
        delivery = ItemDelivery.objects.get(id=pk)
        form = ItemDeliveryForm(request.POST, instance=delivery)
    else:
        return Http404()
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('sparkshed-delivery')
    context = {
        'form': form
    }
    return render(request, 'dashboard/delivery_edit.html', context)


@login_required(login_url='user-login')
def delivery_delete(request, type, pk):
    if type == 'kit':
        delivery = KitDelivery.objects.get(id=pk)
    elif type == 'item':
        delivery = ItemDelivery.objects.get(id=pk)
    else:
        return Http404()
    if request.method == 'POST':
        delivery.delete()
        return redirect('deliveries')
    context = {
        'delivery': delivery
    }
    return render(request, 'dashboard/delivery_delete.html', context)