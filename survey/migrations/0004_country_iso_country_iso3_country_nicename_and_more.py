# Generated by Django 5.1.3 on 2024-11-29 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_remove_samajmemberaddress_taluka_remove_city_taluka_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso',
            field=models.CharField(default='IN', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='iso3',
            field=models.CharField(default='IND', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='nicename',
            field=models.CharField(default='India', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='numcode',
            field=models.CharField(default=356, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='phone_code',
            field=models.PositiveIntegerField(default=91),
            preserve_default=False,
        ),
    ]