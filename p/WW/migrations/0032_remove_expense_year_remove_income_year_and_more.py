# Generated by Django 5.1.4 on 2025-02-25 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0031_expense_year_income_year_financialreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='year',
        ),
        migrations.RemoveField(
            model_name='income',
            name='year',
        ),
        migrations.DeleteModel(
            name='FinancialReport',
        ),
    ]
