# Generated by Django 3.2.9 on 2021-11-15 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_status_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Time'),
        ),
    ]