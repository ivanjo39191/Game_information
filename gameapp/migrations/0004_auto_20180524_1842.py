# Generated by Django 2.0.1 on 2018-05-24 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0003_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamee',
            name='cContent',
            field=models.TextField(blank=True, default='', max_length=255),
        ),
    ]
