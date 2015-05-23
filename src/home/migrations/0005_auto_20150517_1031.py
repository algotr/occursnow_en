# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_auto_20150517_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rating', models.IntegerField(null=True)),
                ('users', models.ManyToManyField(related_name='rated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ratings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='post',
            name='ratings',
            field=models.ForeignKey(null=True, to='home.PostRating'),
            preserve_default=True,
        ),
    ]
