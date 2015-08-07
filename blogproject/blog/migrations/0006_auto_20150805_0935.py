# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_comment_liked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(to='blog.BlogPost'),
        ),
    ]
