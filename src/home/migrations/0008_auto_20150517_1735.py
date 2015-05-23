# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_auto_20150517_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rated_by',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, related_name='rated_posts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='ratings',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
