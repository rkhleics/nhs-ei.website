# Generated by Django 3.1.2 on 2020-10-28 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20201021_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=100, null=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='sub_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='categories.subsite'),
        ),
    ]
