# Generated by Django 5.2.1 on 2025-05-14 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_remove_asset_descrizione_remove_asset_tipo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='descrizione',
            field=models.TextField(blank=True, null=True),
        ),
    ]
