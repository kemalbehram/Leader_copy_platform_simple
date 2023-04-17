# Generated by Django 4.1.7 on 2023-03-07 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0011_remove_traders_users_f_alter_signal_name_trader'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trader_f', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bot.traders')),
                ('user_f', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bot.users')),
            ],
        ),
    ]
