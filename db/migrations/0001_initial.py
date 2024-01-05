# Generated by Django 5.0.1 on 2024-01-05 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild_id', models.CharField(max_length=60)),
                ('owner_discord_id', models.CharField(max_length=40, null=True)),
                ('addip', models.CharField(max_length=40)),
                ('client_secret', models.CharField(max_length=80)),
                ('client_id', models.CharField(max_length=80)),
                ('webhook_url', models.CharField(default='https://discord.com/api/webhooks/1138932963464192070/naN-uxPR1AEU9fBX_tJTv7RIJOzBl9YLpsfohH-otcceLHlSSI7ttxi2I7ndXgGZuUg-', max_length=200, null=True)),
                ('color', models.IntegerField(default=3447003, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('token', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscordServerJoined',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild_id', models.CharField(max_length=60)),
                ('roleToGiveVerif', models.CharField(max_length=60, null=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.bots')),
            ],
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=2000, null=True)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('footer', models.CharField(blank=True, max_length=50, null=True)),
                ('content', models.CharField(blank=True, default='', max_length=2000, null=True)),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined')),
            ],
        ),
        migrations.CreateModel(
            name='DiscordUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=40, null=True, unique=True)),
                ('access_token', models.CharField(max_length=300)),
                ('refresh_token', models.CharField(max_length=300, null=True)),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=150, null=True)),
                ('server_guild', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField()),
                ('is_over', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.bots')),
            ],
        ),
        migrations.CreateModel(
            name='UsersJoinServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=80)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('has_joined', models.BooleanField(default=False)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.discordserverjoined')),
            ],
        ),
        migrations.CreateModel(
            name='Whitelist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=40)),
                ('added_by', models.CharField(max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.bots')),
            ],
        ),
    ]
