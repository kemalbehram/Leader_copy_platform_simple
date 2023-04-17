# Generated by Django 4.1.7 on 2023-03-07 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0006_alter_userfollowing_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowing',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='Bot.traders'),
        ),
        migrations.AlterField(
            model_name='users',
            name='traders',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to='Bot.users'),
        ),
    ]
