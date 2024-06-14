from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from dashboard.helpers import namedtuplefetchall


class ItemManager(models.Manager):
    def with_quantities(self):
        items = list(self.all())
        item_ids = [item.id for item in items]

        # Bulk fetch data for quantity_ordered
        kit_order_sql = f"""
            SELECT ki.item_id, ko.order_quantity, ki.quantity
            FROM dashboard_kitorder ko
            JOIN dashboard_kit k ON ko.kit_id = k.id
            JOIN dashboard_kititem ki ON k.id = ki.kit_id
            LEFT JOIN dashboard_kitdelivery kd ON kd.kit_id = k.id
            WHERE ki.item_id IN ({','.join(map(str, item_ids))})
            AND kd.id IS NULL
        """
        with connection.cursor() as cursor:
            cursor.execute(kit_order_sql)
            kit_order_results = namedtuplefetchall(cursor)

        ordered_from_kits = defaultdict(int)
        for result in kit_order_results:
            ordered_from_kits[result.item_id] += result.order_quantity * result.quantity

        item_orders = ItemOrder.objects.filter(item_id__in=item_ids).values('item_id').annotate(total_order_quantity=Sum('order_quantity'))
        item_deliveries = ItemDelivery.objects.filter(item_id__in=item_ids).values('item_id').annotate(total_order_quantity=Sum('order__order_quantity'))

        ordered_quantities = {order['item_id']: order['total_order_quantity'] for order in item_orders}
        delivered_quantities = {delivery['item_id']: delivery['total_order_quantity'] for delivery in item_deliveries}

        for item in items:
            item._quantity_ordered = ordered_quantities.get(item.id, 0) + ordered_from_kits[item.id]
            item._quantity_delivered = delivered_quantities.get(item.id, 0)

        return items


class Item(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)

    objects = ItemManager()

    def __str__(self):
        return f'{self.name} | quantity: {self.quantity} | ordered: {self.quantity_ordered} | delivered: {self.quantity_delivered}'

    @property
    def quantity_ordered(self):
        if not hasattr(self, '_quantity_ordered'):
            self._quantity_ordered = 0
        return self._quantity_ordered

    @property
    def quantity_delivered(self):
        if not hasattr(self, '_quantity_delivered'):
            self._quantity_delivered = 0
        return self._quantity_delivered

    @property
    def quantity_in_stock(self):
        return self.quantity - self.quantity_delivered


class Kit(models.Model):
    name = models.CharField(max_length=100, null=True)
    updated_date = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kit-detail', kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("kit-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("kit-create-edit", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("kit-delete", kwargs={"id": self.id})

    def get_items_in_kit(self):
        return self.kititems.all()


class KitItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=True, related_name='kititems')
    quantity = models.PositiveIntegerField(null=True)

    def get_absolute_url(self):
        return self.kit.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_id": self.kit.id,
            "id": self.id
        }
        return reverse("kit-item-delete", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.kit.id,
            "id": self.id
        }
        return reverse("kit-item-detail", kwargs=kwargs)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    updated_date = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f'{self.customer}-{self.order_quantity}'

    class Meta:
        abstract = True


class KitOrder(Order):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

    def get_deliver_url(self):
        kwargs = {
            "type": 'kit',
            "order_id": self.id
        }
        return reverse("delivery-create", kwargs=kwargs)

    def is_delivered(self):
        return KitDelivery.objects.filter(order_id=self.id).exists()


class ItemOrder(Order):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Delivery(models.Model):
    delivery_date = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True


class ItemDelivery(Delivery):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(ItemOrder, on_delete=models.CASCADE)

    def clean(self):
        if self.item.quantity < self.order.order_quantity:
            raise ValidationError(f"{self.item.name} quantity cannot exceed amount in stock ({self.item.quantity})")


class KitDelivery(Delivery):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    order = models.ForeignKey(KitOrder, on_delete=models.CASCADE)
