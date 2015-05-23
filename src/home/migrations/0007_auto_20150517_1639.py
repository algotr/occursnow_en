# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20150517_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='ratings',
            field=models.ForeignKey(null=True, to='home.PostRating', blank=True),
            preserve_default=True,
        ),
    ]
