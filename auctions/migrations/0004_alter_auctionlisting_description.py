# Generated by Django 5.0.1 on 2024-01-31 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_id_alter_bid_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(null=True),
        ),
    ]