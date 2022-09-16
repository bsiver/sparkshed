from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Item, Order
from .forms import ItemForm, OrderForm
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
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'form': form,
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
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    product_quantity = Item.objects.filter(name='')
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
    product = Item.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'customer': customer,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def customer_detail(request, pk):
    customer = User.objects.all(groups=2)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    context = {
        'customers': customers,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,

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
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/order.html', context)
