from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from random import randint
from datetime import datetime, timedelta


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    remaining_stock = models.PositiveIntegerField(default=0)
    delivery_period = models.PositiveIntegerField(help_text='Delivery period in days', blank=False, null=False)
    # TODO: Add User reviews and User ratings

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def add_item(self, product, quantity):
        if product.remaining_stock < quantity:
            raise Exception('Quantity is bigger than the available stock!')
        else:
            try:
                cart_item = self.items.get(product=product)
                new_quantity = cart_item.quantity + quantity
                if product.remaining_stock < new_quantity:
                    raise Exception('Quantity is bigger than the available stock!')
                else:
                    cart_item.quantity += quantity
                    cart_item.save()
            except ObjectDoesNotExist:
                cart_item = CartItem(cart_id=self, product=product, quantity=quantity)
                cart_item.save()
        return cart_item

    def remove_item(self, product):
        try:
            cart_item = CartItem.objects.filter(cart_id=self).get(product=product)
            cart_item.delete()
        except ObjectDoesNotExist:
            pass

    def __empty_cart(self):
        for item in self.items.all():
            item.cart_id = None
            item.save()

    def __get_refused_items_from_db(self, items):
        refused_items = []
        for item in items:
            item.product.refresh_from_db()
            if item.product.remaining_stock < item.quantity:
                refused_items.append(item.product.name)
        if refused_items:
            message = '''Product(s) "{}" are not available with the requested quantity
                        Someone might already have ordered them just now!
                        Please refresh your browser and try ordering again'''.format(
                *refused_items
            )
            return message
        return None

    def create_order(self):
        if not self.items.all().count():
            raise Exception('Cart is empty!!')
        message = self.__get_refused_items_from_db(self.items.all())
        if message:
            raise Exception(message)
        order = Order(user=self.user)
        order.save()
        for item in self.items.all():
            item.order_id = order
            item.save()
        order.save()
        self.__empty_cart()

        return order

    def __str__(self):
        return 'Cart:' + str(self.user)


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('Under Preparation', 'Under Preparation'),
        ('Under Shipping', 'Under Shipping'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    order_id = models.CharField(max_length=255, unique=True, editable=False, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Under Preparation')
    expected_delivery_date = models.DateField(editable=False, null=True)

    def save(self):
        # Automatically generating order_id on creation
        if not self.order_id:
            timestamp = str(datetime.now().timestamp()).replace('.', '')
            self.order_id = str(self.user.pk) + str(randint(100, 999)) + timestamp

        # Automatically calculating expected delivery date
        if self.items.all().count():
            max_period = max([item.product.delivery_period for item in self.items.all()])
            self.expected_delivery_date = datetime.now() + timedelta(max_period)

        # Updating the products quantities
        for item in self.items.all():
            item.product.remaining_stock -= item.quantity
            item.product.save()

        super().save()

    def change_status(self, new_status):
        if new_status == 'Cancelled':
            for item in self.items.all():
                item.product.remaining_stock += item.quantity
                item.product.save()
                item.delete()
        self.status = new_status

    def __str__(self):
        return str(self.user) + ':' + self.order_id + ':' + self.status


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_items')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product) + ':' + str(self.quantity)

