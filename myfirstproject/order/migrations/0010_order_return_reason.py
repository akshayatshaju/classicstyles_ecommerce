# Generated by Django 4.2.1 on 2023-07-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='return_reason',
            field=models.TextField(blank=True),
        ),
    ]
