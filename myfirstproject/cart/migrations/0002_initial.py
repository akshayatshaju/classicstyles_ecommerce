# Generated by Django 4.2.1 on 2023-06-29 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productvariant'),
        ),
    ]
