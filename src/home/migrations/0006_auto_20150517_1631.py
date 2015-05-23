# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20150517_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postrating',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
