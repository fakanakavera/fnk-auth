# Generated by Django 5.0 on 2024-01-14 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnk_auth', '0002_customuser_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nick_name',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
