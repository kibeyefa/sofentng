# Generated by Django 3.2.13 on 2022-08-08 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donate', '0002_alter_donateitem_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donateitem',
            name='donator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donator', to=settings.AUTH_USER_MODEL),
        ),
    ]
