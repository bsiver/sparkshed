import json
import logging

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
from .forms import KitItemFormset
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
    items = Item.objects.all()
    kit_orders = KitOrder.objects.all()
    item_orders = ItemOrder.objects.all()
    context = {
        'order': kit_orders.union(item_orders),
        'items': items,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def products(request):
    items = Item.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            item_name = form.cleaned_data.get('name')
            messages.success(request, f'{item_name} has been added')
            return redirect('dashboard-items')
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
            return redirect('dashboard-items')
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
        return redirect('dashboard-items')
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
        return redirect('dashboard-order')
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
        return redirect('dashboard-order')
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


@login_required()
def create_kit(request):
    kit_items = KitItem.objects.all()
    form = KitForm(request.POST or None)
    formset = KitItemFormset(request.POST or None)

    context = {
        'kit_form': form,
        'kit_items_form': formset,
        'kit_items': kit_items
    }
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        kit = form.save()
        for kit_item in formset.forms:
            logger.info(f"{kit_item}")
            kit_item = kit_item.save(commit=False)
            kit_item.kit = kit
            kit_item.save()
            return render(request, "dashboard/kits.html", context)

    logger.info(f"returning {context}")
    return render(request, "dashboard/kit_create.html", context)


@login_required()
def kit_detail(request, id=None):
    if not request.htmx:
        raise Http404
    obj = get_object_or_404(Kit, id=id)
    context = {
        'object': obj,
        'new_kit_item_url': reverse('kit-item-create', kwargs={'parent_id': obj.id})
    }
    return render(request, "partials/kit-details.html", context)


@login_required()
def kit_update(request, id=None):
    obj = get_object_or_404(Kit, id=id)
    form = KitForm(request.POST or None, instance=obj)
    new_kit_item_url = reverse('kit-item-create', kwargs={"parent_id": obj.id})
    context = {
        'form': form,
        'object': obj,
        'new_kit_item_url': new_kit_item_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'
    if request.htmx:
        return render(request, 'partials/forms.html', context)
    return render(request, 'dashboard/kits.html', context)


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


@login_required()
def create_kit_item(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    kit = get_object_or_404(Kit, id=parent_id)
    existing_kit_item = None
    if id is not None:
        try:
            existing_kit_item = KitItem.objects.get(kit=kit, id=id)
        except KitItem.DoesNotExist:
            existing_kit_item = None
    # form = KitItemForm(request.POST or None, instance=existing_kit_item)
    form = KitItemForm()
    url = reverse("kit-item-create", kwargs={"parent_id": kit.id})
    if existing_kit_item:
        url = existing_kit_item.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": existing_kit_item
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if existing_kit_item is None:
            new_obj.kit = kit
        new_obj.save()
        context['object'] = new_obj
        return render(request, "partials/kit-item-inline.html", context)
    return render(request, "partials/kit-item-form.html", context)


@login_required()
def delete_kit_item(request, parent_id=None, id=None):
    kit_item = get_object_or_404(KitItem, kit__id=parent_id, id=id)
    if request.method == "POST":
        name = kit_item.item.name
        kit_item.delete()
        success_url = reverse('kit-detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "partials/kit-item-inline-delete-response.html", {"name": name})
        return redirect(success_url)
    context = {
        "object": kit_item
    }
    return render(request, "dashboard/kit_delete.html", context)


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
    return _create_delivery(request, order_id, type)


def _create_delivery(request, order_id, delivery_type):
    if delivery_type == 'item':
        order = get_object_or_404(ItemOrder, id=order_id)
        delivery = ItemDelivery(item=order.item, order=order)
        form = ItemDeliveryForm(instance=delivery)
    elif delivery_type == 'kit':
        order = get_object_or_404(KitOrder, id=order_id)
        delivery = KitDelivery(kit=order.kit, order=order)
        form = KitDeliveryForm({'kit': order.kit, 'order': order}, instance=delivery)
    else:
        raise Http404()

    if not form.is_valid():
        return HttpResponseBadRequest(headers={
            'HX-Trigger': json.dumps({
                "showMessage": f"{form.errors}"
            })
        })

    obj = form.save(commit=False)
    obj.customer = request.user
    obj.clean()
    obj.save()
    if request.htmx:
        return HttpResponse(
            status=200,
            headers={
                'HX-Trigger': json.dumps({
                    "showMessage": f"Delivery created!"
                })
            })

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
        return redirect('dashboard-delivery')
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