import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ItemForm
from .forms import ItemOrderForm
from .forms import KitForm
from .forms import KitItemForm
from .forms import KitOrderForm
from .models import Item
from .models import ItemOrder
from .models import Kit
from .models import KitItem
from .models import KitOrder
from .models import Order

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def index(request):
    items = Item.objects.all()
    order = Order.objects.all()
    context = {
        'order': order,
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
#@allowed_users(allowed_roles=['Admin'])
def customers(request):
    customer = User.objects.all()
    context = {
        'customer': customer,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def customer_detail(request, pk):
    customers = User.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
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
#@allowed_users(allowed_roles=['Admin'])
def item_delete(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-items')
    context = {
        'item': item
    }
    return render(request, 'dashboard/items_delete.html', context)


#@login_required(login_url='user-login')
def order(request):
    kit_orders = list(KitOrder.objects.all())
    item_orders = list(ItemOrder.objects.all())

    # if request.method == 'POST':
    #     logger.info(request.POST)
    #     kit_form = KitOrderForm(request.POST)
    #     item_form = None
    #     if kit_form.is_valid():
    #         obj = kit_form.save(commit=False)
    #         obj.customer = request.user
    #         obj.save()
    #         return redirect('dashboard-order')
    kit_form = KitOrderForm()
    item_form = ItemOrderForm()

    context = {
        'item_form': item_form,
        'kit_form': kit_form,
        'new_kit_order_url': reverse('kit-order-create'),
        'item_orders': item_orders,
        'kit_orders': kit_orders
    }
    return render(request, 'dashboard/order.html', context)

#@login_required(login_url='user-login')
def kit_order(request):
    form = KitOrderForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.customer = request.user
        obj.save()
        if request.htmx:
            return render(request)
    return redirect('dashboard-order')

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def order_edit(request, pk):
    order = KitOrder.objects.get(id=pk)
    if request.method == 'POST':
        form = KitOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard-order')
    else:
        form = KitOrderForm(instance=order)
    context = {
        'form': form
    }
    return render(request, 'dashboard/order_edit.html', context)

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard-order')
    context = {
        'order': order
    }
    return render(request, 'dashboard/order_delete.html', context)


@login_required()
def create_kit(request):
    form = KitForm(request.POST or None)
    kit_items = KitItem.objects.all()
    context = {
        'form': form,
        'kit_items': kit_items
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.customer = request.user
        obj.save()
        context['new_kit_item_url'] = reverse('kit-item-create', kwargs={"parent_id": obj.id})
        if request.htmx:
            logger.info(f'ret {context}')
            return render(request, "partials/kit-details.html", context)
        return redirect(obj.get_absolute_url())
    return render(request, "dashboard/kit-create-update.html", context)


@login_required()
def kit_detail(request, id=None):
    if not request.htmx:
        raise Http404
    obj = get_object_or_404(Kit, id=id)
    context = {
        'object': obj,
        'new_kit_item_url': reverse('kit-item-create', kwargs={'parent_id': obj.id})
    }
    logger.info(f'ctx {context}')
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
    return render(request, 'dashboard/kit-create-update.html', context)


@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
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
    logger.info(f'called with {parent_id} {id}')
    if not request.htmx:
        raise Http404
    kit = get_object_or_404(Kit, id=parent_id)
    existing_kit_item = None
    if id is not None:
        try:
            existing_kit_item = KitItem.objects.get(kit=kit, id=id)
        except KitItem.DoesNotExist:
            existing_kit_item = None
    form = KitItemForm(request.POST or None, instance=existing_kit_item)
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
    logger.info(f'getting ctx {context}')
    return render(request, "partials/kit-item-form.html", context)


@login_required()
def delete_kit_item(request, parent_id=None, id=None):
    kit_item = get_object_or_404(KitItem, kit__id=parent_id, id=id)
    if request.method == "POST":
        name = kit_item.name
        kit_item.delete()
        success_url = reverse('kit-detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "partials/kit-item-inline-delete-response.html", {"name": name})
        return redirect(success_url)
    context = {
        "object": kit_item
    }
    return render(request, "dashboard/kit_delete.html", context)
