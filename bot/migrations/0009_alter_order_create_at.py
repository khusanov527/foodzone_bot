# Generated by Django 3.2.3 on 2022-02-20 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_order_create_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
