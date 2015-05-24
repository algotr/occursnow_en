# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20150524_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postrating',
            name='users',
        ),
        migrations.DeleteModel(
            name='PostRating',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='ratings',
            new_name='rate_down',
        ),
        migrations.AddField(
            model_name='post',
            name='rate_up',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
