from django.contrib.auth.models import User

from dashboard.models import Item
from dashboard.models import ItemDelivery
from dashboard.models import ItemOrder
from dashboard.models import Kit
from dashboard.models import KitDelivery
from dashboard.models import KitOrder


def stats_bar(request):
    kit_count = Kit.objects.all().count()
    customer_count = User.objects.all().count()
    item_count = Item.objects.all().count()
    order_count = KitOrder.objects.all().count() + ItemOrder.objects.all().count()
    delivery_count = KitDelivery.objects.all().count() + ItemDelivery.objects.all().count()

    return {
        'customer_count': customer_count,
        'item_count': item_count,
        'order_count': order_count,
        'kit_count': kit_count,
        'delivery_count': delivery_count
    }