# Generated by Django 2.2.2 on 2019-10-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_auto_20191020_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='storypost',
            name='tags',
            field=models.TextField(default='<django.db.models.fields.TextField>', editable=False, max_length=200),
        ),
        migrations.AddField(
            model_name='storypost',
            name='title',
            field=models.TextField(default='6UXlg0Vq', editable=False, max_length=200),
        ),
    ]