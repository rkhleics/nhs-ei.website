# Generated by Django 3.1.4 on 2020-12-14 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('home', '0011_auto_20201214_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='hero_heading',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
