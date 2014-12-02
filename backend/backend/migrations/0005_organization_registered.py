# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20141202_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='registered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
