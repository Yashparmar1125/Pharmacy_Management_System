# Generated by Django 5.1 on 2024-09-19 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='city',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='country',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='state',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]
