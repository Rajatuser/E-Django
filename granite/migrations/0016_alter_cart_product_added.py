# Generated by Django 4.0.4 on 2022-04-22 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('granite', '0015_remove_cart_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_added',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_added', to='granite.product'),
        ),
    ]
