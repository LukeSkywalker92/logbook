# Generated by Django 3.1 on 2020-08-22 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0003_auto_20200822_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbook',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='logbookentry',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='logbookentry',
            name='loogbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='database.logbook'),
        ),
    ]