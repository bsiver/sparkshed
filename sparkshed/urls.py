from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from user import views as user_views


urlpatterns = [
    path('index/', views.index, name='sparkshed-index'),
    path('items/', views.products, name='sparkshed-items'),
    path('items/delete/<int:pk>/', views.item_delete, name='sparkshed-items-delete'),
    path('items/detail/<int:pk>/', views.item_detail, name='sparkshed-items-detail'),
    path('items/edit/<int:pk>/', views.item_edit, name='sparkshed-items-edit'),
    path('items/order/', views.item_order, name='item-order-create'),
    path('customers/', views.customers, name='sparkshed-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail, name='sparkshed-customer-detail'),

    # orders
    path('order/', views.order, name='sparkshed-order'),
    path('order/delete/<str:type>/<int:pk>/', views.order_delete, name='sparkshed-order-delete'),
    path('order/detail/<str:type>/<int:pk>/', views.order_edit, name='sparkshed-order-edit'),

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

    # admin & user routes
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='user-register'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('profile/', user_views.profile, name='user-profile'),
    path('profile/update/', user_views.profile_update, name='user-profile-update'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
