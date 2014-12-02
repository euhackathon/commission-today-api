# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_portofolio_shorthand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('money', models.IntegerField()),
                ('lobbyists', models.IntegerField()),
                ('lobbyists_with_access', models.IntegerField()),
                ('explore_url', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='organization',
            field=models.ForeignKey(to='backend.Organization', null=True),
            preserve_default=True,
        ),
    ]
