# Generated by Django 5.1.4 on 2025-02-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0014_rename_expensename_expense_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='frequency',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='month',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='name',
        ),
        migrations.RemoveField(
            model_name='income',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='income',
            name='frequency',
        ),
        migrations.RemoveField(
            model_name='income',
            name='month',
        ),
        migrations.RemoveField(
            model_name='income',
            name='name',
        ),
        migrations.AddField(
            model_name='expense',
            name='source',
            field=models.CharField(default='12.21 as a value', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='source',
            field=models.CharField(default='12.21 as a value', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='emoji',
            field=models.CharField(default='🛒', max_length=5),
        ),
        migrations.AlterField(
            model_name='income',
            name='emoji',
            field=models.CharField(default='💰', max_length=5),
        ),
    ]
