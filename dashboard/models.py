from django.db import models
from django.contrib.auth.models import User


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


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.customer}-{self.item}'
