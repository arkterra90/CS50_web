# Generated by Django 4.2.2 on 2023-09-23 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_postlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likeCount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]