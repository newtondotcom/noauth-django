# Generated by Django 4.2.2 on 2023-08-18 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("db", "0005_discordserver_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discordserver",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db.discordusers"
            ),
        ),
    ]
