# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-10 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='party_image',
            field=models.ImageField(blank=True, upload_to='users/party_logo/'),
        ),
    ]
