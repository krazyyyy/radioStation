# Generated by Django 3.2.6 on 2021-11-22 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0005_auto_20211108_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=200)),
                ('radio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_genre', to='stations.radiolist')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('radio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_category', to='stations.radiolist')),
            ],
        ),
        migrations.AddField(
            model_name='radiolist',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='radio_country', to='stations.countries'),
        ),
    ]
