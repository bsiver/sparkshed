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
    path('order/', views.order, name='dashboard-order'),
    path('order/delete/<str:type>/<int:pk>/', views.order_delete, name='dashboard-order-delete'),
    path('order/detail/<str:type>/<int:pk>/', views.order_edit, name='dashboard-order-edit'),
    path('kit/', views.create_kit, name='kits'),
    path('kit/create/', views.create_kit, name='kit-create'),
    path('kit/order/', views.kit_order, name='kit-order-create'),
    path('kit/delete/<int:id>/', views.kit_delete, name='kit-delete'),
    path('kit/edit/<int:id>/', views.kit_update, name='kit-edit'),
    path('kit/detail/<int:id>/', views.kit_detail, name='kit-detail'),

    # kit items
    path('<int:parent_id>/kit_item/create', views.create_kit_item, name='kit-item-create'),
    path('<int:parent_id>/kit_item/detail/<int:id>/', views.create_kit_item, name='kit-item-detail'),
    path('<int:parent_id>/kit_item/delete/<int:id>/', views.delete_kit_item, name='kit-item-delete'),
]
