# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.IntegerField(choices=[(1, b'Monday'), (2, b'Tuesday'), (3, b'Wednesday'), (4, b'Thursday'), (5, b'Friday'), (6, b'Saturday'), (7, b'Sunday')])),
                ('fromHour', models.TimeField()),
                ('toHour', models.TimeField()),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField()),
                ('_tables', models.TextField(default=b'2,2,4,4')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='openingtime',
            name='restaurant',
            field=models.ForeignKey(related_name=b'opening_times', to='restaurant.Restaurant'),
            preserve_default=True,
        ),
    ]
