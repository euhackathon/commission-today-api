# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20141203_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='organization',
            field=models.ForeignKey(blank=True, to='backend.Organization', null=True),
            preserve_default=True,
        ),
    ]
