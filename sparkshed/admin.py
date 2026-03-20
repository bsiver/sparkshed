from django.contrib import admin
from .models import Item, ItemDelivery, ItemOrder
from .models import Kit, KitItem, KitDelivery, KitOrder


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'description')
    search_fields = ('name', 'description')
    list_filter = ('quantity',)


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'order_quantity', 'recipient', 'created_date')
    search_fields = ('customer__username', 'recipient', 'item__name')
    list_filter = ('created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')


class ItemDeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'order', 'delivery_date')
    search_fields = ('item__name', 'order__customer__username')
    list_filter = ('delivery_date',)
    readonly_fields = ('delivery_date',)


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_date')
    search_fields = ('name',)
    list_filter = ('updated_date',)


class KitItemAdmin(admin.ModelAdmin):
    list_display = ('kit', 'item', 'quantity')
    search_fields = ('kit__name', 'item__name')


class KitOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'kit', 'order_quantity', 'recipient', 'created_date')
    search_fields = ('customer__username', 'recipient', 'kit__name')
    list_filter = ('created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')


class KitDeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'kit', 'order', 'delivery_date')
    search_fields = ('kit__name', 'order__customer__username')
    list_filter = ('delivery_date',)
    readonly_fields = ('delivery_date',)


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemOrder, ItemOrderAdmin)
admin.site.register(ItemDelivery, ItemDeliveryAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(KitOrder, KitOrderAdmin)
admin.site.register(KitItem, KitItemAdmin)
admin.site.register(KitDelivery, KitDeliveryAdmin)
