# Generated by Django 2.0.3 on 2018-04-24 21:19

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anmeldung', '0019_club_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='ranking_points',
            field=models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
    ]
