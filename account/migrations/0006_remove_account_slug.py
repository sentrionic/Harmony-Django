# Generated by Django 2.2.2 on 2019-10-22 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='slug',
        ),
    ]
