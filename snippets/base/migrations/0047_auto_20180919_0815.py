# Generated by Django 2.1 on 2018-09-19 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_auto_20180917_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='publish_end',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='publish_start',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='target',
        ),
        migrations.AddField(
            model_name='asrsnippet',
            name='publish_end',
            field=models.DateTimeField(blank=True, help_text='See the current time in <a href="http://time.is/UTC">UTC</a>', null=True, verbose_name='Publish Ends'),
        ),
        migrations.AddField(
            model_name='asrsnippet',
            name='publish_start',
            field=models.DateTimeField(blank=True, help_text='See the current time in <a href="http://time.is/UTC">UTC</a>', null=True, verbose_name='Publish Starts'),
        ),
        migrations.AddField(
            model_name='asrsnippet',
            name='target',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.Target'),
        ),
    ]
