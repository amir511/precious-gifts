# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-05 18:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_add_shipping_fees'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingfees',
            options={'verbose_name_plural': 'Shipping Fees'},
        ),
    ]
