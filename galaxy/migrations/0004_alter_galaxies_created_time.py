# Generated by Django 4.1 on 2023-03-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("galaxy", "0003_userclassifyrecord_last_change_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="galaxies",
            name="created_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]