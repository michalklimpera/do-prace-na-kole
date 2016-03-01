# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 16:58
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.gis.geos import MultiLineString


def change_line_to_multiline(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    UserAttendance  = apps.get_model("dpnk", "UserAttendance")
    for ua in UserAttendance.objects.all():
        if ua.track:
            ua.multi_track = MultiLineString([ua.track, ])
            ua.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0011_auto_20160227_1657'),
    ]

    operations = [
        migrations.RunPython(change_line_to_multiline),
    ]
