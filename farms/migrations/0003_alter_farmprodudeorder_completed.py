# Generated by Django 3.2.13 on 2022-07-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0002_farmproduce_unit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmprodudeorder',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]