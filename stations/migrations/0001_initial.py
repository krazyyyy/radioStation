# Generated by Django 3.2.6 on 2021-11-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RadioList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radio_name', models.CharField(max_length=200)),
            ],
        ),
    ]