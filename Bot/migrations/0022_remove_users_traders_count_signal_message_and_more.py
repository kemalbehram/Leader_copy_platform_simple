# Generated by Django 4.1.7 on 2023-04-17 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0021_alter_users_subscription_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='traders_count',
        ),
        migrations.AddField(
            model_name='signal',
            name='message',
            field=models.CharField(default=12, max_length=3000, verbose_name='Message'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='traders',
            name='is_active',
            field=models.BooleanField(default=False, help_text='If the check box is active, the trader"s trades are copied ', verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='users',
            name='balance',
            field=models.FloatField(default=0, verbose_name='User balance {cashback}'),
        ),
        migrations.AlterField(
            model_name='users',
            name='subscription_type',
            field=models.CharField(choices=[('Free', 'Free'), ('VIP', 'VIP')], default='Free', max_length=25, verbose_name='Subscription type'),
        ),
        migrations.DeleteModel(
            name='UserFollowing',
        ),
    ]
