# -*- coding: utf-8 -*-
# Generated by Django 1.9.5.dev20160321164524 on 2016-03-30 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0022_auto_20160328_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='company_admin_count',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]