# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=64)),
                ('pubDate', models.DateField()),
                ('slug', models.SlugField()),
                ('body', models.TextField()),
                ('summary', models.TextField()),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=64)),
                ('pubDate', models.DateField()),
                ('body', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(to='blog.BlogPost')),
            ],
        ),
    ]
