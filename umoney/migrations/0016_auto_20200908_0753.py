# Generated by Django 3.1 on 2020-09-08 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0015_topupcheckreq_topupcheckresp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionaggregationinquiryreq',
            old_name='closing_gate',
            new_name='closing_date',
        ),
    ]