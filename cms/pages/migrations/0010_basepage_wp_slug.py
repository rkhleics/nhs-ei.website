# Generated by Django 3.1.2 on 2020-10-22 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20201021_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='basepage',
            name='wp_slug',
            field=models.TextField(null=True),
        ),
    ]
