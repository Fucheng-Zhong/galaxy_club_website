# Generated by Django 4.1 on 2023-03-22 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("galaxy", "0002_alter_userclassifyrecord_galaxy_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userclassifyrecord",
            name="last_change_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="userclassifyrecord",
            name="created_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]