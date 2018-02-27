# Generated by Django 2.0.1 on 2018-02-22 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitetree_modeltranslation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeltranslationtreeitem',
            name='description_dsnkcs',
            field=models.TextField(blank=True, default='', help_text='Additional comments on this item.', null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='modeltranslationtreeitem',
            name='hint_dsnkcs',
            field=models.CharField(blank=True, default='', help_text='Some additional information about this item that is used as a hint.', max_length=200, null=True, verbose_name='Hint'),
        ),
        migrations.AddField(
            model_name='modeltranslationtreeitem',
            name='title_dsnkcs',
            field=models.CharField(help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='modeltranslationtreeitem',
            name='url_dsnkcs',
            field=models.CharField(db_index=True, help_text='Exact URL or URL pattern (see "Additional settings") for this item.', max_length=200, null=True, verbose_name='URL'),
        ),
    ]
