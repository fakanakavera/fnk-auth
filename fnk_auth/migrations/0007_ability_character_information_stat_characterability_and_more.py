# Generated by Django 5.0 on 2024-01-18 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnk_auth', '0006_remove_useraccountdetails_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('discovered_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnk_auth.ability')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_abilities', to='fnk_auth.character')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='abilities',
            field=models.ManyToManyField(through='fnk_auth.CharacterAbility', to='fnk_auth.ability'),
        ),
        migrations.CreateModel(
            name='CharacterInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=False)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_information', to='fnk_auth.character')),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnk_auth.information')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='known_information',
            field=models.ManyToManyField(blank=True, through='fnk_auth.CharacterInformation', to='fnk_auth.information'),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='fnk_auth.player'),
        ),
        migrations.CreateModel(
            name='CharacterStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_stats', to='fnk_auth.character')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnk_auth.stat')),
            ],
            options={
                'unique_together': {('character', 'stat')},
            },
        ),
        migrations.AddField(
            model_name='character',
            name='stats',
            field=models.ManyToManyField(through='fnk_auth.CharacterStat', to='fnk_auth.stat'),
        ),
        migrations.CreateModel(
            name='StatToAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnk_auth.ability')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnk_auth.stat')),
            ],
            options={
                'unique_together': {('stat', 'ability')},
            },
        ),
        migrations.AddField(
            model_name='ability',
            name='stats',
            field=models.ManyToManyField(related_name='abilities', through='fnk_auth.StatToAbility', to='fnk_auth.stat'),
        ),
    ]