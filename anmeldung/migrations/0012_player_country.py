# Generated by Django 2.0.3 on 2018-03-21 19:55

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('anmeldung', '0011_auto_20180320_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='country',
            field=django_countries.fields.CountryField(default='DE', max_length=2),
            preserve_default=False,
        ),
    ]
