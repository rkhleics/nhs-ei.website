# Generated by Django 3.1.2 on 2020-10-14 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20201006_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='wp_id',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
