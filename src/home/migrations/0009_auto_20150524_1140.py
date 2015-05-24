# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20150517_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postrating',
            old_name='rating',
            new_name='vote_down',
        ),
        migrations.AddField(
            model_name='postrating',
            name='vote_up',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
