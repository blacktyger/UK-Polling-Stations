# Generated by Django 3.2 on 2021-09-28 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_finder", "0013_increase_referer_field_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loggedpostcode",
            name="has_election",
            field=models.BooleanField(null=True),
        ),
    ]
