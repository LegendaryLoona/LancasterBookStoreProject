# Generated by Django 5.1.2 on 2024-11-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_delete_globalconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='years',
            field=models.IntegerField(default=30),
        ),
    ]
