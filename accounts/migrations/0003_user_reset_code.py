# Generated by Django 3.2.9 on 2021-11-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_activation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
