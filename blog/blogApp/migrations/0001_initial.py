# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 21:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=100)),
                ('article_desc', models.CharField(blank=True, max_length=100)),
                ('article_body', models.TextField(blank=True, max_length=200)),
                ('article_img', models.ImageField(blank=True, default='images_folder/none/no-img.jpg', upload_to='images_folder/articles')),
                ('article_add_date', models.DateTimeField(auto_now_add=True)),
                ('article_update_date', models.DateField(auto_now=True)),
                ('article_status', models.CharField(choices=[('R', 'DRAFT'), ('P', 'PUBLISHED'), ('D', 'DELETED')], default='R', max_length=30)),
                ('article_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.CharField(max_length=1000)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment_article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogApp.Article')),
                ('reply', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blogApp.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'ADMIN'), ('E', 'EDITOR'), ('R', 'REGULAR')], default='R', max_length=30)),
                ('image', models.ImageField(blank=True, default='images_folder/none/no-img.jpg', upload_to='images_folder/articles')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='article_tags',
            field=models.ManyToManyField(to='blogApp.Tag'),
        ),
    ]