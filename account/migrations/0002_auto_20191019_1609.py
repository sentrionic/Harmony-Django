# Generated by Django 2.2.2 on 2019-10-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='phone number'),
        ),
    ]
