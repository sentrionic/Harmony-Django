# Generated by Django 2.2.2 on 2019-10-21 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0007_auto_20191021_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypost',
            name='title',
            field=models.TextField(default='gx4m2A01', editable=False, max_length=200),
        ),
    ]