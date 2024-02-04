# Generated by Django 5.0.1 on 2024-02-04 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.URLField(blank=True, default='https://via.placeholder.com/500', null=True),
        ),
    ]