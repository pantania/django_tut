# Generated by Django 3.0.6 on 2020-05-21 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_account_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alert',
            field=models.BooleanField(default=False),
        ),
    ]
