# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0026_blinkquestion_current'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlinkAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
            ],
            options={
                'verbose_name': 'blinkassignment',
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='blinkassignments',
            field=models.ManyToManyField(to='peerinst.BlinkAssignment', blank=True),
        ),
    ]
