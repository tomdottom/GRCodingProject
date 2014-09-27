# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('people', models.IntegerField()),
                ('restaurant', models.ForeignKey(related_name=b'reservations', to='restaurant.Restaurant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
