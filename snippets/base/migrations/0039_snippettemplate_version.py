# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_auto_20180604_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippettemplate',
            name='version',
            field=models.CharField(default='1.0.0', max_length=10),
            preserve_default=False,
        ),
    ]
