# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150805_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]
