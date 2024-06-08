from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='dashboard-index'),
    path('items/', views.products, name='dashboard-items'),
    path('items/delete/<int:pk>/', views.item_delete, name='dashboard-items-delete'),
    path('items/detail/<int:pk>/', views.item_detail, name='dashboard-items-detail'),
    path('items/edit/<int:pk>/', views.item_edit, name='dashboard-items-edit'),
    path('items/order/', views.item_order, name='item-order-create'),
    path('customers/', views.customers, name='dashboard-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail, name='dashboard-customer-detail'),

    # orders
    path('order/', views.order, name='dashboard-order'),
    path('order/delete/<str:type>/<int:pk>/', views.order_delete, name='dashboard-order-delete'),
    path('order/detail/<str:type>/<int:pk>/', views.order_edit, name='dashboard-order-edit'),

    # deliveries
    path('deliveries/', views.delivery, name='deliveries'),
    path('delivery/delete/<str:type>/<int:pk>/', views.delivery_delete, name='delivery-delete'),
    path('delivery/detail/<str:type>/<int:pk>/', views.delivery_edit, name='delivery-edit'),
    path('delivery/<str:type>/<int:order_id>/', views.create_delivery, name='delivery-create'),

    # kits
    path('kit/', views.kit, name='kits'),
    path('kit/create/', views.create_or_edit_kit, name='kit-create-edit'),
    path('kit/order/', views.kit_order, name='kit-order-create'),
    path('kit/delete/<int:id>/', views.kit_delete, name='kit-delete'),
    path('kit/edit/<int:id>/', views.create_or_edit_kit, name='kit-create-edit'),
]
