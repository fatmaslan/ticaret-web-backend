# Generated by Django 5.1.6 on 2025-03-12 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modaapp', '0023_sliderimages_slider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='images',
        ),
        migrations.AddField(
            model_name='sliderimages',
            name='slider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sliderimages', to='modaapp.slider'),
        ),
    ]
