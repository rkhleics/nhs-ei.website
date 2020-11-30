# Generated by Django 3.1.2 on 2020-10-30 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20201028_1347'),
        ('blogs', '0003_auto_20201030_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='sub_site_categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category_blog_site', to='categories.categorysubsite'),
        ),
    ]
