# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-23 09:13
from __future__ import unicode_literals

from django.db import migrations
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20190105_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_summary',
            field=djangocms_text_ckeditor.fields.HTMLField(),
        ),
    ]
