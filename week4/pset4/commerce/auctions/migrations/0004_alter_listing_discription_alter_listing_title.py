# Generated by Django 4.2.2 on 2023-07-05 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='discription',
            field=models.TextField(verbose_name='Listing Discription'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Listing Title'),
        ),
    ]
