from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from random import randint
from datetime import datetime, timedelta


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=False, null=False)
    image = FilerImageField(blank=True, null=True)
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
                ','.join(refused_items)
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
            item.product.remaining_stock -= item.quantity
            item.product.save()
            item.save()
        order.save()
        self.__empty_cart()

        return order

    @property
    def total_price(self):
        shipping_fees = ShippingFees.objects.all()[0].amount if ShippingFees.objects.all().count() else 0
        price = 0
        for item in self.items.all():
            price += item.price

        return price + shipping_fees

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', editable=False, null=True)
    order_summary = HTMLField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Under Preparation')
    expected_delivery_date = models.DateField(editable=False, null=True)


    def __generate_order_summary(self):
        SUMMARY_TEMPLATE = """
        <b>Order summary:</b>
        <hr>
        <p>Order id: {order_id}</p>
        <p>User name: {username}</p>
        <p>User email: {user_email}</p>
        <p>User phone: {user_phone}</p>
        <p>Shipping address: {shipping_address}</p>
        <p>Expected delivery date: {delivery_date}</p>
        <p>Total price: {total_price} L.E.</p>
        <u>Items:</u>
        {items}
        """
        items_string = ''
        for item in self.items.all():
            s = '<p>product: ' + item.product.name + ', quantity: ' + str(item.quantity) + '</p>'
            items_string += s

        summary = SUMMARY_TEMPLATE.format(
            order_id=self.order_id,
            username=self.user.username,
            user_email=self.user.email,
            user_phone=self.user.buyer.phone_number,
            shipping_address=self.user.buyer.shipping_address,
            delivery_date=self.expected_delivery_date,
            total_price = self.total_price,
            items=items_string
        )
        return summary

    def save(self, *args, **kwargs):
        # Automatically generating order_id on creation
        if not self.order_id:
            timestamp = str(datetime.now().timestamp()).replace('.', '')
            self.order_id = str(self.user.pk) + str(randint(100, 999)) + timestamp

        # Automatically calculating expected delivery date
        if self.items.all().count():
            max_period = max([item.product.delivery_period for item in self.items.all()])
            self.expected_delivery_date = datetime.now() + timedelta(max_period)

        # Handle the changes in status
        self._change_status(self.status)

        # Generate order summary
        self.order_summary = self.__generate_order_summary()

        super().save(*args, **kwargs)

    def _change_status(self, new_status):
        if new_status == 'Cancelled':
            for item in self.items.all():
                item.product.remaining_stock += item.quantity
                item.product.save()
                item.delete()

    @property
    def total_price(self):
        shipping_fees = ShippingFees.objects.all()[0].amount if ShippingFees.objects.all().count() else 0
        price = 0
        for item in self.items.all():
            price += item.price

        return price + shipping_fees

    def __str__(self):
        return str(self.user) + ':' + self.order_id + ':' + self.status


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_items')
    quantity = models.PositiveIntegerField()

    @property
    def price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product) + ':' + str(self.quantity)

class ShippingFees(models.Model):
    class Meta:
        verbose_name_plural = 'Shipping Fees'
    
    amount = models.FloatField(blank=False, null=False)

    def clean(self):
        old_fees_exists = self.__class__.objects.all().count()
        if old_fees_exists and not self.pk:
            raise ValidationError('Cannot add more than one record for shipping fees!')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return 'Shipping Fees:' + str(self.amount)