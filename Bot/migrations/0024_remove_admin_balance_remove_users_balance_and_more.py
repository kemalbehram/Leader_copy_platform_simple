# Generated by Django 4.1.7 on 2023-04-17 08:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0023_alter_traders_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='users',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='users',
            name='referral',
        ),
        migrations.AddField(
            model_name='admin',
            name='percent_balance',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Percent allocated for order'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='admin',
            field=models.BooleanField(default=True, help_text='If user admin true/else false', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='user_id',
            field=models.CharField(max_length=30, unique=True, verbose_name='User or Channel ID in Telegram'),
        ),
    ]
