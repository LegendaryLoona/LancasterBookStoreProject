# Generated by Django 5.1.2 on 2024-10-31 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_globalconfig_alter_expense_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]
