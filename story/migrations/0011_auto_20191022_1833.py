# Generated by Django 2.2.2 on 2019-10-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0010_auto_20191021_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypost',
            name='title',
            field=models.TextField(default='2SO6KhvJ', editable=False, max_length=200),
        ),
    ]
