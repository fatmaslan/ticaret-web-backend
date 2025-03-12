# Generated by Django 5.1.6 on 2025-03-10 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modaapp', '0020_alter_cartitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='categories', to='modaapp.category'),
        ),
    ]
