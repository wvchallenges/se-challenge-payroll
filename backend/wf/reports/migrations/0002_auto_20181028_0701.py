# Generated by Django 2.1.2 on 2018-10-28 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timereportentry',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timereportentry',
            name='hours_worked',
            field=models.FloatField(),
        ),
    ]
