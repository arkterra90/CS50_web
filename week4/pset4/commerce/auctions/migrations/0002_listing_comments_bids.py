# Generated by Django 4.2.2 on 2023-07-05 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('discription', models.TextField()),
                ('condition', models.CharField(choices=[('New', 'New'), ('Used', 'Used')], default='', max_length=5)),
                ('list_user', models.IntegerField()),
                ('list_time', models.DateTimeField(auto_now_add=True)),
                ('list_pic', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_comment', models.TextField()),
                ('user_comment', models.IntegerField()),
                ('time_comment', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
            ],
        ),
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('bid_time', models.DateTimeField(auto_now_add=True)),
                ('bid_user', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
            ],
        ),
    ]