from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django.urls import reverse

from dashboard.helpers import namedtuplefetchall


class Item(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def quantity_ordered(self):
        kit_order_sql = f"""
            SELECT ko.order_quantity, ki.quantity
            FROM dashboard_kitorder ko
            JOIN dashboard_kit k ON ko.kit_id = k.id
            JOIN dashboard_kititem ki on ko.kit_id = k.id
            JOIN dashboard_item i ON i.id = ki.item_id
            WHERE ki.item_id = {self.id}
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(kit_order_sql)
        with connection.cursor() as cursor:
            cursor.execute(kit_order_sql)
            results = namedtuplefetchall(cursor)

        ordered_from_kits = 0
        if results:
            ordered_from_kits = sum([i.order_quantity * i.quantity for i in results])

        return sum([order.order_quantity for order in ItemOrder.objects.filter(item__name=self.name)]) + ordered_from_kits

    @property
    def quantity_remaining(self):
        return self.quantity - self.quantity_ordered


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
        return reverse("kit-edit", kwargs={"id": self.id})

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


class ItemOrder(Order):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
