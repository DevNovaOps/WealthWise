# Generated by Django 5.1.4 on 2025-02-24 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0027_alter_user_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='currency',
        ),
    ]
