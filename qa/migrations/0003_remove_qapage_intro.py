# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-04 18:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_qapage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qapage',
            name='intro',
        ),
    ]
