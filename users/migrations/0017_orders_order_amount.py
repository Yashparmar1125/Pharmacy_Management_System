# Generated by Django 5.1 on 2024-10-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
