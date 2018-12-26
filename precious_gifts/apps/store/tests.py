from django.test import TestCase
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.models import User
from datetime import datetime
from math import ceil


class StoreAppTest(TestCase):
    def setUp(self):
        self.u1 = User(username='u1', password='u1_password')
        self.u2 = User(username='u2', password='u2_password')
        self.u1.save()
        self.u2.save()
        self.p1 = Product(name='p1', price=1, remaining_stock=2, delivery_period=3)
        self.p2 = Product(name='p2', price=1, remaining_stock=3, delivery_period=5)
        self.p3 = Product(name='p3', price=1, remaining_stock=1, delivery_period=2)
        self.p1.save()
        self.p2.save()
        self.p3.save()
        self.c1 = Cart(user=self.u1)
        self.c2 = Cart(user=self.u2)
        self.c1.save()
        self.c2.save()

    def test_normal_order(self):
        # Adding an item
        self.c1.add_item(self.p1, 1)
        self.c1.save()
        # Check item is p1
        self.assertEqual(self.c1.items.all()[0].product, self.p1)
        # Remove item and assert cart is empty
        self.c1.remove_item(self.p1)
        self.assertEqual(self.c1.items.all().count(), 0)
        # create order
        self.c1.add_item(self.p1, 1)
        o1 = self.c1.create_order()
        # check delivery period is correct
        order_delivery_preiod = ceil(((((o1.expected_delivery_date - datetime.now()).total_seconds()) / 60) / 60) / 24)
        self.assertEqual(order_delivery_preiod, self.p1.delivery_period)
        # Assert items removed from cart after creating order
        self.assertEqual(self.c1.items.all().count(), 0)
        # Make sure items were added to order
        self.assertEqual(o1.items.all()[0].product, self.p1)
        # Make sure product quantity was updated
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 1)
        # Change Order Status
        o1.change_status('Delivered')
        self.assertEqual(o1.status, 'Delivered')
        # Cancel order and check product qty
        o1.change_status('Cancelled')
        o1.save()
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 2)

    def test_quantity_issues(self):
        ERROR_MESSAGE = 'Quantity is bigger than the available stock!'
        # Trying to add items with exactly the same quantity available
        self.assertIsInstance(self.c1.add_item(self.p1, 2), CartItem)
        # Trying to add items higher than available
        self.c1.remove_item(self.p1)
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE):
            self.c1.add_item(self.p1, 3)

        # Now adding item normally
        self.c1.add_item(self.p1, 2)
        self.c1.save()
        # Now trying to add items again in the same session
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE):
            self.c1.add_item(self.p1, 1)
        # Now checking cart out
        self.c1.create_order()
        # check cart is now empty
        self.assertEqual(self.c1.items.all().count(), 0)
        # Assert p1 now doesn't have remaining stock
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 0)
        # Again trying to add items to cart
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE):
            self.c1.add_item(self.p1, 1)

    def test_multiple_orders_for_same_item(self):
        ERROR_MESSAGE = 'are not available with the requested quantity'
        self.c1.add_item(self.p1, 2)
        self.c2.add_item(self.p1, 1)
        o1 = self.c1.create_order()
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE):
            self.c2.create_order()
        o1.change_status('Cancelled')
        o1.save()
        self.assertEqual(self.p1.remaining_stock, 2)
        self.assertIsInstance(self.c2.create_order(), Order)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 1)

    def test_cart_with_many_items(self):
        ERROR_MESSAGE = 'Quantity is bigger than the available stock!'
        self.c1.add_item(self.p1, 2)
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE):
            self.c1.add_item(self.p2, 4)
        self.c1.add_item(self.p2, 3)
        self.c1.add_item(self.p3, 1)
        o1 = self.c1.create_order()
        self.assertIsInstance(o1, Order)
        self.assertEqual(self.c1.items.all().count(), 0)
        self.assertEqual(o1.items.all().count(), 3)
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.p3.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 0)
        self.assertEqual(self.p2.remaining_stock, 0)
        self.assertEqual(self.p3.remaining_stock, 0)
        o1.change_status('Cancelled')
        o1.save()
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.p3.refresh_from_db()
        self.assertEqual(self.p1.remaining_stock, 2)
        self.assertEqual(self.p2.remaining_stock, 3)
        self.assertEqual(self.p3.remaining_stock, 1)

    def test_multiple_orders_same_item_diversed_carts(self):
        ERROR_MESSAGE = 'Product(s) "{}" are not available with the requested quantity'
        self.c1.add_item(self.p1, 1)
        self.c1.add_item(self.p2, 2)
        self.c2.add_item(self.p1, 2)
        self.c2.add_item(self.p2, 1)
        self.c1.create_order()
        self.assertEqual(self.c1.items.all().count(), 0)
        with self.assertRaisesMessage(Exception, ERROR_MESSAGE.format(self.p1.name)):
            self.c2.create_order()
        self.assertNotEqual(self.c2.items.all().count(), 0)

    def test_create_order_with_empty_cart(self):
        with self.assertRaisesMessage(Exception, 'Cart is empty!!'):
            # Create order
            self.c1.create_order()

    def test_refused_message_includes_all_items(self):
        self.c1.add_item(self.p1, 2)
        self.c1.add_item(self.p2, 3)
        self.c1.add_item(self.p3, 1)
        self.c2.add_item(self.p1, 2)
        self.c2.add_item(self.p2, 3)
        self.c2.add_item(self.p3, 1)
        self.c1.create_order()
        with self.assertRaisesMessage(Exception, 'Product(s) "p1,p2,p3" are not available with the requested quantity'):
            # Create order
            self.c2.create_order()
