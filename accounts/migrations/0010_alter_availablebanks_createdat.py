# Generated by Django 3.2.13 on 2022-09-06 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_availablebanks_useraccountnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablebanks',
            name='createdAt',
            field=models.DateTimeField(),
        ),
    ]