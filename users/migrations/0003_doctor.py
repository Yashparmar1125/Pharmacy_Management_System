# Generated by Django 5.1 on 2024-09-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_profile_pic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('specialization', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
    ]
