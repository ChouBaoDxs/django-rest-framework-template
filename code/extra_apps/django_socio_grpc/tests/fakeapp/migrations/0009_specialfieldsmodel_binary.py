# Generated by Django 3.2.11 on 2022-02-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fakeapp", "0008_auto_20220128_1022"),
    ]

    operations = [
        migrations.AddField(
            model_name="specialfieldsmodel",
            name="binary",
            field=models.BinaryField(default=None),
        ),
    ]
