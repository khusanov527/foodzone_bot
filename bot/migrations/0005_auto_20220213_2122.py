# Generated by Django 3.2.3 on 2022-02-13 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20220213_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
