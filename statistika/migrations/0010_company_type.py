# Generated by Django 4.2 on 2023-05-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistika', '0009_remove_company_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.ManyToManyField(null=True, to='statistika.businesstype'),
        ),
    ]