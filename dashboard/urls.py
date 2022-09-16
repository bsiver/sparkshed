from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='dashboard-index'),
    path('items/', views.products, name='dashboard-items'),
    path('items/delete/<int:pk>/', views.item_delete,
         name='dashboard-items-delete'),
    path('items/detail/<int:pk>/', views.item_detail,
         name='dashboard-items-detail'),
    path('items/edit/<int:pk>/', views.item_edit,
         name='dashboard-items-edit'),
    path('customers/', views.customers, name='dashboard-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail,
         name='dashboard-customer-detail'),
    path('order/', views.order, name='dashboard-order'),
]
