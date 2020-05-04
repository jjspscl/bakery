# Generated by Django 3.0.5 on 2020-05-04 10:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200503_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastry',
            name='gpp',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
