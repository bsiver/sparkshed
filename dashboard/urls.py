from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='dashboard-index'),
    path('items/', views.products, name='dashboard-items'),
    path('items/delete/<int:pk>/', views.item_delete, name='dashboard-items-delete'),
    path('items/detail/<int:pk>/', views.item_detail, name='dashboard-items-detail'),
    path('items/edit/<int:pk>/', views.item_edit, name='dashboard-items-edit'),
    path('customers/', views.customers, name='dashboard-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail, name='dashboard-customer-detail'),
    path('order/', views.order, name='dashboard-order'),
    path('order/delete/<int:pk>/', views.order_delete, name='dashboard-order-delete'),
    path('order/detail/<int:pk>/', views.order_edit, name='dashboard-order-edit'),
    path('kit/', views.kits, name='kits'),
    path('kit/create/', views.kits, name='kit-create'),
    path('kit/delete/<int:pk>/', views.order_delete, name='dashboard-kit-delete'),
    path('kit/detail/<int:pk>/', views.order_edit, name='dashboard-kit-edit'),
]
