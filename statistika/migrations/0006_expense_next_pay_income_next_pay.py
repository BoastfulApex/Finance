# Generated by Django 4.1.4 on 2023-03-27 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistika', '0005_expense_often_expense_status_income_often_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='next_pay',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='next_pay',
            field=models.DateField(blank=True, null=True),
        ),
    ]
