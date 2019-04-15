# Generated by Django 2.1.5 on 2019-03-13 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0073_newslettertemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendToDeviceTemplate',
            fields=[
                ('template_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.Template')),
                ('scene1_title', models.CharField(blank=True, help_text='Snippet title displayed before snippet text.', max_length=255)),
                ('scene1_text', models.TextField(help_text='Main body text of snippet. HTML subset allowed: i, b, u, strong, em, br.')),
                ('scene1_button_label', models.CharField(default='Learn more', help_text='Label for the button on Scene 1 that leads to Scene 2.', max_length=50)),
                ('scene1_button_color', models.CharField(blank=True, help_text='The text color of the button. Valid CSS color. Defaults to Firefox Theme Color.', max_length=20)),
                ('scene1_button_background_color', models.CharField(blank=True, help_text='The background color of the button. Valid CSS color. Defaults to Firefox Theme Color.', max_length=20)),
                ('scene2_title', models.CharField(blank=True, help_text='Title displayed before text in scene 2.', max_length=255)),
                ('scene2_text', models.TextField(help_text='Scene 2 main text. HTML subset allowed: i, b, u, strong, em, br.')),
                ('scene2_button_label', models.CharField(default='Send', help_text='Label for form submit button.', max_length=50)),
                ('scene2_input_placeholder', models.CharField(default='Your email here', help_text='Placeholder text for email / phone number field.', max_length=255)),
                ('scene2_dismiss_button_text', models.CharField(default='Dismiss', help_text='Label for the dismiss button on Scene 2.', max_length=50)),
                ('scene2_disclaimer_html', models.TextField(help_text='Text and link underneath the input box.')),
                ('locale', models.CharField(default='en-US', help_text='Two to five character string for the locale code. Default "en-US".', max_length=10)),
                ('country', models.CharField(default='us', help_text='Two character string for the country code (used for SMS). Default "us".', max_length=10)),
                ('include_sms', models.BooleanField(blank=True, default=False, help_text='Defines whether SMS is available.')),
                ('message_id_sms', models.CharField(blank=True, help_text='Newsletter/basket id representing the SMS message to be sent.', max_length=100)),
                ('message_id_email', models.CharField(help_text='Newsletter/basket id representing the email message to be sent. Must be a value from the "Slug" column here: https://basket.mozilla.org/news/.', max_length=100)),
                ('success_title', models.TextField(help_text='Title of success message after form submission.')),
                ('success_text', models.TextField(help_text='Text of success message after form submission.')),
                ('error_text', models.TextField(help_text='Text of error message if form submission fails.')),
                ('block_button_text', models.CharField(default='Remove this', help_text='Tooltip text used for dismiss button.', max_length=50)),
                ('do_not_autoblock', models.BooleanField(blank=True, default=False, help_text='Used to prevent blocking the snippet after the CTA (link or button) has been clicked.')),
                ('scene1_icon', models.ForeignKey(help_text='Snippet icon. 192x192 PNG.', on_delete=django.db.models.deletion.CASCADE, related_name='sendtodevice_scene1_icons', to='base.Icon')),
                ('scene1_title_icon', models.ForeignKey(blank=True, help_text='Small icon that shows up before the title / text. 64x64px.PNG. Grayscale.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sendtodevice_scene1_title_icons', to='base.Icon')),
                ('scene2_icon', models.ForeignKey(help_text='Image to display above the form. 192x192px PNG.', on_delete=django.db.models.deletion.CASCADE, related_name='sendtodevice_scene2_icons', to='base.Icon')),
            ],
            bases=('base.template',),
        ),
    ]