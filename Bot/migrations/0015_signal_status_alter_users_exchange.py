# Generated by Django 4.1.7 on 2023-03-09 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0014_alter_users_exchange_alter_users_subscription_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='signal',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='exchange',
            field=models.CharField(choices=[('Not_connect', 'Not_connect'), ('Binance', 'Binance'), ('Bybit', 'Bybit')], default='Not_connect', max_length=25, verbose_name='Exchange'),
        ),
    ]
