# Generated by Django 3.2.9 on 2021-11-14 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_categories_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='status',
            new_name='active',
        ),
    ]
