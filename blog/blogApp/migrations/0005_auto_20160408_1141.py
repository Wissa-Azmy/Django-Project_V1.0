# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-08 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0004_auto_20160408_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_img',
            field=models.ImageField(blank=True, default='images_folder/none/no-img.jpg', upload_to='/Applications/MAMP/htdocs/Django-Project/static_in_env/media_root/images_folder/articles'),
        ),
    ]
