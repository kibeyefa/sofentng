# Generated by Django 3.2.13 on 2022-08-21 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0008_alter_farmprodudeorder_produce'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='farmprodudeorder',
            options={'ordering': ['id']},
        ),
    ]
