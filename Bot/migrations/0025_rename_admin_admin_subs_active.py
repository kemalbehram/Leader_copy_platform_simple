# Generated by Django 4.1.7 on 2023-04-18 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0024_remove_admin_balance_remove_users_balance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='admin',
            new_name='subs_active',
        ),
    ]
