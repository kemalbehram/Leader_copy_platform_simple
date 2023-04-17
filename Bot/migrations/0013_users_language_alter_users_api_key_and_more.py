# Generated by Django 4.1.7 on 2023-03-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0012_userfollowing'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='language',
            field=models.CharField(choices=[('ru', 'ru'), ('en', 'en')], default='en', max_length=10, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='users',
            name='api_key',
            field=models.CharField(blank=True, max_length=350, verbose_name='Exchange api key'),
        ),
        migrations.AlterField(
            model_name='users',
            name='api_secret',
            field=models.CharField(blank=True, max_length=350, verbose_name='Exchange api secret'),
        ),
        migrations.AlterField(
            model_name='users',
            name='subscription_type',
            field=models.CharField(choices=[('Free', 'Free'), ('Ordinary', 'Ordinary'), ('Standard', 'Standard'), ('VIP', 'VIP')], default='Free', max_length=10, verbose_name='Subscription type'),
        ),
    ]
