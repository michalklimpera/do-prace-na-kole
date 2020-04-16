# Generated by Django 2.2.11 on 2020-04-02 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0150_merge_20200327_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='commutemode',
            name='distance_important',
            field=models.BooleanField(default=True, verbose_name='Je vzdalenost důležité'),
        ),
        migrations.AddField(
            model_name='commutemode',
            name='duration_important',
            field=models.BooleanField(default=True, verbose_name='Je vzdalenost důležité'),
        ),
        migrations.AddField(
            model_name='commutemode',
            name='minimum_distance',
            field=models.FloatField(default=0, verbose_name='Minimální vzdalenost (km)'),
        ),
        migrations.AddField(
            model_name='commutemode',
            name='minimum_duration',
            field=models.PositiveIntegerField(default=0, verbose_name='Minimální doba ve sekundách'),
        ),
        migrations.AlterField(
            model_name='dpnknotificationtemplate',
            name='icon',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]