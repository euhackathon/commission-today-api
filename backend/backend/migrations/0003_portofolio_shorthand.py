# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20141202_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='portofolio',
            name='shorthand',
            field=models.CharField(default=b'', max_length=128),
            preserve_default=True,
        ),
    ]
