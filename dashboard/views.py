from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Item
from .models import Kit
from .models import Order
from .forms import ItemForm
from .forms import KitItemFormset
from .forms import OrderForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .decorators import auth_users, allowed_users
# Create your views here.


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
    order = Order.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-order')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'dashboard/order.html', context)

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def order_edit(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard-order')
    else:
        form = OrderForm(instance=order)
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


#@login_required(login_url='user-login')
def kits(request):
    kits = Kit.objects.all()

    if request.method == 'POST':
        form = KitItemFormset(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-kit')
    else:
        form = KitItemFormset()

    context = {
        'form': form,
        'kits': kits
    }
    return render(request, 'dashboard/kit.html', context)


def kits(request):
    qs = Kit.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "dashboard/kit.html", context)

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def kit_edit(request, pk):
    kit = Kit.objects.get(id=pk)
    if request.method == 'POST':
        form = KitForm(request.POST, instance=kit)
        if form.is_valid():
            form.save()
            return redirect('dashboard-kit')
    else:
        form = KitForm(instance=kit)
    context = {
        'form': form
    }
    return render(request, 'dashboard/kit_edit.html', context)

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def kit_delete(request, pk):
    kit = Kit.objects.get(id=pk)
    if request.method == 'POST':
        kit.delete()
        return redirect('dashboard-kit')
    context = {
        'kit': kit
    }
    return render(request, 'dashboard/kit_delete.html', context)