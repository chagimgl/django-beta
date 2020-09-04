# Generated by Django 3.1 on 2020-09-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0004_auto_20200904_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionResp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message_type_id', models.CharField(blank=True, default='', max_length=4)),
                ('primary_bit_map', models.CharField(blank=True, default='', max_length=16)),
                ('processing_code', models.CharField(blank=True, default='', max_length=6)),
                ('transmission_datetime', models.CharField(blank=True, default='', max_length=10)),
                ('transaction_unique', models.CharField(blank=True, default='', max_length=12)),
                ('response_code', models.CharField(blank=True, default='', max_length=2)),
                ('merchant_id', models.CharField(blank=True, default='', max_length=15)),
                ('merchant_info_terminal_id', models.CharField(blank=True, default='', max_length=10)),
                ('result_message_len', models.CharField(blank=True, default='', max_length=3)),
                ('result_message_data', models.CharField(blank=True, default='', max_length=64)),
                ('response_data_len', models.CharField(blank=True, default='', max_length=3)),
                ('working_key', models.CharField(blank=True, default='', max_length=32)),
                ('minimum_topup_amount', models.CharField(blank=True, default='', max_length=10)),
                ('system_datetime', models.CharField(blank=True, default='', max_length=14)),
                ('pos_id', models.CharField(blank=True, default='', max_length=64)),
                ('terminal_id', models.CharField(blank=True, default='', max_length=64)),
                ('authentication_id', models.CharField(blank=True, default='', max_length=64)),
            ],
        ),
    ]
