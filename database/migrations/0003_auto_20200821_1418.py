# Generated by Django 3.1 on 2020-08-21 14:18

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200821_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logbookentry',
            name='text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]