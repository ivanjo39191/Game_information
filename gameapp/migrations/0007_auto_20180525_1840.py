# Generated by Django 2.0.1 on 2018-05-25 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0006_auto_20180525_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamee',
            name='cAuthor',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
