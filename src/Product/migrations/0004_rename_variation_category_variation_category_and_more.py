# Generated by Django 5.1.2 on 2024-10-20 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Product", "0003_variation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="variation",
            old_name="variation_category",
            new_name="category",
        ),
        migrations.RenameField(
            model_name="variation",
            old_name="variation_value",
            new_name="value",
        ),
    ]
