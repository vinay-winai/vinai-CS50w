# Generated by Django 4.1 on 2022-09-28 18:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0012_alter_listing_curr_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="curr_bid",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(99999999.99),
                ]
            ),
        ),
    ]
