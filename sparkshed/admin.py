from django.contrib import admin
from .models import Item
from .models import ItemOrder
from .models import Kit
from .models import KitItem
from .models import KitOrder


# Register your models here.
admin.site.register(Item)
admin.site.register(ItemOrder)
admin.site.register(Kit)
admin.site.register(KitOrder)
admin.site.register(KitItem)
