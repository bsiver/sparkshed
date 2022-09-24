from django.contrib.auth.models import User

from dashboard.models import Kit, Item, Order


def stats_bar(request):
    kit_count = Kit.objects.all().count()
    customer_count = User.objects.all().count()
    item_count = Item.objects.all().count()
    order_count = Order.objects.all().count()

    return {
        'customer_count': customer_count,
        'item_count': item_count,
        'order_count': order_count,
        'kit_count': kit_count,
    }