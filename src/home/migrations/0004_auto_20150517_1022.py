# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150512_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='votes',
        ),
        migrations.AddField(
            model_name='post',
            name='ratings',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
