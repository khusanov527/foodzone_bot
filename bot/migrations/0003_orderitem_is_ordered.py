# Generated by Django 3.2.3 on 2022-02-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20220210_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]