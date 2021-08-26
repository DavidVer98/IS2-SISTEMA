# Generated by Django 3.2.6 on 2021-08-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=50)),
                ('estado', models.CharField(default='PENDIENTE', max_length=100)),
                ('fecha_inicio', models.DateField()),
            ],
        ),
    ]
