# Generated by Django 2.2.2 on 2019-10-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_auto_20191021_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypost',
            name='title',
            field=models.TextField(default='gtzhF4C4', editable=False, max_length=200),
        ),
    ]
