# Generated by Django 4.1.7 on 2023-03-06 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Bot', '0002_alter_users_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Families',
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
        migrations.AlterModelOptions(
            name='users',
            options={},
        ),
        migrations.AlterField(
            model_name='users',
            name='traders',
            field=models.ManyToManyField(blank=True, related_name='users', to='Bot.traders'),
        ),
    ]
