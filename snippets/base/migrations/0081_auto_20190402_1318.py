# Generated by Django 2.1.7 on 2019-04-02 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0080_auto_20190401_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asrsnippet',
            name='data',
        ),
        migrations.RemoveField(
            model_name='asrsnippet',
            name='template',
        ),
    ]
