# Generated by Django 2.0.1 on 2018-05-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0005_auto_20180524_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamee',
            name='cContent',
            field=models.TextField(blank=True, default='', max_length=99999),
        ),
    ]
