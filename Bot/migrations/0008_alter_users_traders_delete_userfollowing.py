# Generated by Django 4.1.7 on 2023-03-07 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0007_alter_userfollowing_user_id_alter_users_traders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='traders',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to='Bot.traders'),
        ),
        migrations.DeleteModel(
            name='UserFollowing',
        ),
    ]
