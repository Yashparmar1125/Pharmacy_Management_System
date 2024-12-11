# Generated by Django 5.1 on 2024-09-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_medicine_med_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone_no', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True)),
                ('age', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]
