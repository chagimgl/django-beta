# Generated by Django 3.1 on 2020-09-09 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umoney', '0018_auto_20200909_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topupresp',
            name='vsam_id',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
