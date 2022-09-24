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
from .decorators import auth_users, allowed_users
# Create your views here.


@login_required(login_url='user-login')
def index(request):
    items = Item.objects.all()
    item_count = items.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter()
    customer_count = customer.count()
    context = {
        'order': order,
        'items': items,
        'item_count': item_count,
        'order_count': order_count,
        'customer_count': customer_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def products(request):
    items = Item.objects.all()
    item_count = items.count()
    customer = User.objects.filter()
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    product_quantity = Item.objects.filter(name='')
    kit_count = Kit.objects.all().count()
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
        'form': form,
        'customer_count': customer_count,
        'item_count': item_count,
        'order_count': order_count,
        'kit_count': kit_count
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
    customer_count = customer.count()
    items = Item.objects.all()
    item_count = items.count()
    order = Order.objects.all()
    order_count = order.count()
    kit_count = Kit.objects.all().count()
    context = {
        'customer': customer,
        'customer_count': customer_count,
        'item_count': item_count,
        'order_count': order_count,
        'kit_count': kit_count
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def customer_detail(request, pk):
    customer = User.objects.all()
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    kit_count = Kit.objects.all.count()

    context = {
        'customers': customers,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
        'kit_count': kit_count
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
    order_count = order.count()
    customer = User.objects.filter()
    customer_count = customer.count()
    items = Item.objects.all()
    item_count = items.count()
    kit_count = Kit.objects.all().count()

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
        'customer_count': customer_count,
        'item_count': item_count,
        'kit_count': kit_count,
        'order_count': order_count,
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
    kit_count = kits.count()
    customer = User.objects.filter()
    customer_count = customer.count()
    items = Item.objects.all()
    item_count = items.count()
    order_count = Order.objects.all().count()

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
        'kits': kits,
        'customer_count': customer_count,
        'item_count': item_count,
        'order_count': order_count,
        'kit_count': kit_count,
    }
    return render(request, 'dashboard/kit.html', context)

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