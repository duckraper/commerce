# Generated by Django 5.0.1 on 2024-02-03 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auctionlisting_starting_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
