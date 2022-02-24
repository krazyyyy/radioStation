# Generated by Django 3.2.6 on 2021-12-02 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0011_rssfeed_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssfeed',
            name='source_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_radio', to='stations.radiolist'),
        ),
    ]
