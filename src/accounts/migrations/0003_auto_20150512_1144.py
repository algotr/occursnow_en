# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150506_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(to='accounts.UserProfile', blank=True, related_name='followed_by'),
            preserve_default=True,
        ),
    ]
