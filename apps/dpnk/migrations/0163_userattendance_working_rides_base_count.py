# Generated by Django 2.2.20 on 2021-05-03 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0162_auto_20210503_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattendance',
            name='working_rides_base_count',
            field=models.FloatField(editable=False, null=True),
        ),
    ]