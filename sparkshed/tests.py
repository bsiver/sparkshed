from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Item, Kit, KitItem, ItemOrder, KitOrder, ItemDelivery, KitDelivery


class ItemModelTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Test Item', quantity=100, description='A test item')

    def test_item_creation(self):
        """Test that an item can be created"""
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.quantity, 100)

    def test_item_quantity_in_stock(self):
        """Test that quantity_in_stock calculates correctly"""
        self.assertEqual(self.item.quantity_in_stock, 100)


class KitModelTests(TestCase):
    def setUp(self):
        self.kit = Kit.objects.create(name='Test Kit')
        self.item1 = Item.objects.create(name='Item 1', quantity=50, description='Item 1')
        self.item2 = Item.objects.create(name='Item 2', quantity=100, description='Item 2')

    def test_kit_creation(self):
        """Test that a kit can be created"""
        self.assertEqual(self.kit.name, 'Test Kit')

    def test_kit_add_items(self):
        """Test that items can be added to a kit"""
        KitItem.objects.create(kit=self.kit, item=self.item1, quantity=2)
        KitItem.objects.create(kit=self.kit, item=self.item2, quantity=5)
        self.assertEqual(self.kit.kititems.count(), 2)


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item = Item.objects.create(name='Test Item', quantity=100, description='Test')
        self.kit = Kit.objects.create(name='Test Kit')
        KitItem.objects.create(kit=self.kit, item=self.item, quantity=5)

    def test_item_order_creation(self):
        """Test that an item order can be created"""
        order = ItemOrder.objects.create(
            customer=self.user,
            item=self.item,
            order_quantity=10,
            recipient='Test Recipient'
        )
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.order_quantity, 10)

    def test_kit_order_creation(self):
        """Test that a kit order can be created"""
        order = KitOrder.objects.create(
            customer=self.user,
            kit=self.kit,
            order_quantity=5,
            recipient='Test Recipient'
        )
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.order_quantity, 5)

    def test_kit_order_deliver_url_valid(self):
        """Test that KitOrder.get_deliver_url() returns a valid URL"""
        order = KitOrder.objects.create(
            customer=self.user,
            kit=self.kit,
            order_quantity=5,
            recipient='Test Recipient'
        )
        url = order.get_deliver_url()
        self.assertIn('sparkshed-delivery-create', url)
        self.assertIn('kit', url)


class ItemDeliveryValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item = Item.objects.create(name='Test Item', quantity=10, description='Test')
        self.order1 = ItemOrder.objects.create(
            customer=self.user,
            item=self.item,
            order_quantity=5,
            recipient='Recipient 1'
        )
        self.order2 = ItemOrder.objects.create(
            customer=self.user,
            item=self.item,
            order_quantity=5,
            recipient='Recipient 2'
        )

    def test_item_delivery_validation_with_existing_delivery(self):
        """Test that ItemDelivery.clean() accounts for already-delivered stock"""
        # First delivery of 5 items
        delivery1 = ItemDelivery(item=self.item, order=self.order1)
        delivery1.clean()  # Should not raise
        delivery1.save()

        # Second delivery of 5 items should fail (only 10 in stock, 5 already delivered)
        delivery2 = ItemDelivery(item=self.item, order=self.order2)
        with self.assertRaises(ValidationError):
            delivery2.clean()

    def test_item_delivery_validation_sufficient_stock(self):
        """Test that ItemDelivery.clean() passes with sufficient stock"""
        order = ItemOrder.objects.create(
            customer=self.user,
            item=self.item,
            order_quantity=5,
            recipient='Test'
        )
        delivery = ItemDelivery(item=self.item, order=order)
        delivery.clean()  # Should not raise


class ViewAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_profile_view_requires_login(self):
        """Test that profile view redirects unauthenticated users"""
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url.lower())

    def test_profile_view_accessible_when_authenticated(self):
        """Test that profile view is accessible when authenticated"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_requires_login(self):
        """Test that profile update view redirects unauthenticated users"""
        response = self.client.get(reverse('user-profile-update'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url.lower())


class DeliveryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item = Item.objects.create(name='Test Item', quantity=50, description='Test')
        self.order = ItemOrder.objects.create(
            customer=self.user,
            item=self.item,
            order_quantity=10,
            recipient='Test Recipient'
        )

    def test_create_delivery_get_does_not_save(self):
        """Test that GET to create_delivery does not save a delivery record"""
        self.client.login(username='testuser', password='testpass')
        initial_count = ItemDelivery.objects.count()
        response = self.client.get(
            reverse('sparkshed-delivery-create', args=['item', self.order.id])
        )
        self.assertEqual(ItemDelivery.objects.count(), initial_count)

    def test_create_delivery_post_saves(self):
        """Test that POST to create_delivery saves a delivery record"""
        self.client.login(username='testuser', password='testpass')
        initial_count = ItemDelivery.objects.count()
        response = self.client.post(
            reverse('sparkshed-delivery-create', args=['item', self.order.id]),
            data={}
        )
        # Delivery should be created
        self.assertEqual(ItemDelivery.objects.count(), initial_count + 1)


class OrderDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.kit = Kit.objects.create(name='Test Kit')
        self.order = KitOrder.objects.create(
            customer=self.user,
            kit=self.kit,
            order_quantity=5,
            recipient='Test'
        )

    def test_order_delete_invalid_type_returns_404(self):
        """Test that invalid order type returns 404"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('sparkshed-order-delete', args=['invalid', self.order.id])
        )
        self.assertEqual(response.status_code, 404)


class ManagementCommandTests(TestCase):
    def test_createsu_is_idempotent(self):
        """Test that createsu command doesn't fail when called twice"""
        from django.core.management import call_command
        from io import StringIO

        # First call should create the user
        call_command('createsu', stdout=StringIO())
        self.assertTrue(User.objects.filter(username='admin').exists())
        first_user = User.objects.get(username='admin')

        # Second call should not create a duplicate
        call_command('createsu', stdout=StringIO())
        self.assertEqual(User.objects.filter(username='admin').count(), 1)
        second_user = User.objects.get(username='admin')

        # Should be the same user
        self.assertEqual(first_user.id, second_user.id)
