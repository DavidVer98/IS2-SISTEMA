# Generated by Django 3.2.6 on 2021-08-26 20:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0002_proyecto_scrum_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='scrum_master',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='miembros',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]