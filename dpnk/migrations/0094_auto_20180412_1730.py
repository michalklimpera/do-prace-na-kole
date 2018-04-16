# Generated by Django 2.0.2 on 2018-04-12 17:30

import django.core.validators
from django.db import migrations, models
import stdnumfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0093_auto_20180323_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='slug_identifier',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Identifikátor kampaně'),
        ),
        migrations.AlterField(
            model_name='company',
            name='dic',
            field=stdnumfield.models.StdNumField(alphabets=[None], blank=True, default='', error_messages={'stdnum_format': 'DIČ není zadáno ve správném formátu. Zkontrolujte že číslo má 8 až 10 číslic a případně ho doplňte nulami zleva. Číslu musí předcházet dvě písmena identifikátoru země (např. CZ)'}, formats=['cz.dic'], null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]{2}[0-9]*$', 'DIČ musí být číslo uvozené dvoupísmeným identifikátorem státu.')], verbose_name='DIČ'),
        ),
    ]
