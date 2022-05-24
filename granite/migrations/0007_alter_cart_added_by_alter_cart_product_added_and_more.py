# Generated by Django 4.0.4 on 2022-04-21 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('granite', '0006_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='added_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='addedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_added',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_added', to='granite.product'),
        ),
        migrations.AlterField(
            model_name='like',
            name='product_liked',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_liked', to='granite.product'),
        ),
    ]
