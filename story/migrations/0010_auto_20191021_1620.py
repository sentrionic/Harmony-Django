# Generated by Django 2.2.2 on 2019-10-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0009_auto_20191021_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypost',
            name='title',
            field=models.TextField(default='41NjrF4R', editable=False, max_length=200),
        ),
    ]
