# -*- coding: utf-8 -*-
# Generated by Django 1.9.5.dev20160321164524 on 2016-06-02 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0031_auto_20160531_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='show_results',
            field=models.BooleanField(default=True, verbose_name='Zobrazovat výsledky soutěže'),
        ),
    ]
