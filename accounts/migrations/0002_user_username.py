# Generated by Django 3.2.13 on 2022-07-11 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='kibeyefa', max_length=255),
            preserve_default=False,
        ),
    ]
