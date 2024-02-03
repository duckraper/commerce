# Generated by Django 5.0.1 on 2024-02-03 03:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_user_listings_made'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listings_made',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='made_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listings_made', to=settings.AUTH_USER_MODEL),
        ),
    ]
