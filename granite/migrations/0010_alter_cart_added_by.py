# Generated by Django 4.0.4 on 2022-04-21 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('granite', '0009_alter_like_liked_by_alter_like_product_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addedBy', to=settings.AUTH_USER_MODEL),
        ),
    ]
