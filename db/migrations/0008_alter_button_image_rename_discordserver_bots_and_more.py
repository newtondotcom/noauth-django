# Generated by Django 4.2.2 on 2023-08-31 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_button_delete_myservermembers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='image',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.RenameModel(
            old_name='DiscordServer',
            new_name='Bots',
        ),
        migrations.CreateModel(
            name='DiscordServerJoined',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild_id', models.CharField(max_length=60)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.bots')),
            ],
        ),
        migrations.AlterField(
            model_name='button',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined'),
        ),
        migrations.AlterField(
            model_name='discordusers',
            name='server_guild',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined'),
        ),
        migrations.AlterField(
            model_name='serverjoins',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined'),
        ),
    ]
