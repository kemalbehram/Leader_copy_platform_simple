# Generated by Django 4.1.7 on 2023-03-11 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0017_users_referral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='referral',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='Bot.users'),
        ),
    ]
