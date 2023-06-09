# Generated by Django 4.1.7 on 2023-03-07 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0004_alter_users_traders_delete_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='traders',
            field=models.ManyToManyField(blank=True, related_name='users', to='Bot.traders'),
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='Bot.users')),
            ],
        ),
    ]
