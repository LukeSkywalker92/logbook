# Generated by Django 3.1 on 2020-08-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_logbook_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbook',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
    ]
