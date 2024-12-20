# Generated by Django 5.1 on 2024-10-24 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_orders_order_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('exp_id', models.AutoField(primary_key=True, serialize=False)),
                ('expense_type', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('expense_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incomes',
            fields=[
                ('income_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True)),
                ('income_type', models.CharField(max_length=50)),
                ('income_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
