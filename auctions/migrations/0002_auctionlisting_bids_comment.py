# Generated by Django 3.2.11 on 2022-01-30 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auctionTitle', models.CharField(max_length=64)),
                ('auctionDescription', models.TextField()),
                ('auctionStartBid', models.DecimalField(decimal_places=2, max_digits=19)),
                ('auctionImageURL', models.URLField()),
                ('auctionCategory', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
