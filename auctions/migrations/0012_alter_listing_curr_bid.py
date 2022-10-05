# Generated by Django 4.1 on 2022-09-28 18:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_bid_item_alter_bid_new_bid_alter_listing_curr_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="curr_bid",
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(99999999.99),
                ],
            ),
        ),
    ]
