# Generated by Django 4.2.2 on 2023-07-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_listing_list_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bid_current',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid_user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
