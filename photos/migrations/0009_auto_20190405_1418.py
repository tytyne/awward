# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-05 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_auto_20190329_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='occupation',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]