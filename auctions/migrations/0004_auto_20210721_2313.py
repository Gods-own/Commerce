# Generated by Django 3.2.5 on 2021-07-21 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='Item',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='Listing',
            new_name='listing',
        ),
    ]
