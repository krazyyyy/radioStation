# Generated by Django 3.2.6 on 2021-11-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0004_radiohistory_radiosession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radiolist',
            name='radio_host',
        ),
        migrations.AddField(
            model_name='radiolist',
            name='radio_img',
            field=models.ImageField(blank=True, null=True, upload_to='radiobanner'),
        ),
    ]
