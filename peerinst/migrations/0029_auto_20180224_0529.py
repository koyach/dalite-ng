# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0028_blinkquestion_blinkassignment'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='blinkquestion',
            order_with_respect_to='blinkassignment',
        ),
    ]
