# Generated by Django 4.1.7 on 2023-03-06 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dm_backend", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equation",
            name="line_style",
            field=models.CharField(
                choices=[
                    ("-", "SOLID"),
                    ("--", "DASHED"),
                    (":", "DOTTED"),
                    ("-.", "DASH_DOT"),
                ],
                default="-",
                max_length=5,
            ),
        ),
    ]
