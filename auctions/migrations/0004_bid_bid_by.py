# Generated by Django 3.2 on 2022-03-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_won_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_by',
            field=models.CharField(default='None', max_length=64),
        ),
    ]
