# Generated by Django 5.1.3 on 2024-12-05 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_country_iso_country_iso3_country_nicename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='samajmemberoccupation',
            name='company_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
