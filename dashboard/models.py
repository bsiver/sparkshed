from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def quantity_ordered(self):
        return sum([order.order_quantity for order in Order.objects.filter(item__name=self.name)])

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
        return self.kititem_set.all()


class KitItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def get_absolute_url(self):
        return self.kit.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_id": self.kit.id,
            "id": self.id
        }
        return reverse("kit-item-create", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.kit.id,
            "id": self.id
        }
        return reverse("kit-item-detail", kwargs=kwargs)


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    updated_date = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f'{self.customer}-{self.item}'
