# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0027_auto_20180224_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='blinkquestion',
            name='blinkassignment',
            field=models.ManyToManyField(to='peerinst.BlinkAssignment', blank=True),
        ),
    ]
