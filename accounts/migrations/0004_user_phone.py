# Generated by Django 3.2.13 on 2022-07-15 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='08114843722', max_length=11),
            preserve_default=False,
        ),
    ]
