# Generated by Django 2.1.1 on 2018-10-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_auto_20181004_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='ready_for_review',
            field=models.BooleanField(default=False),
        ),
    ]