# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='bookingstep',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='phone',
            field=models.CharField(default=datetime.datetime(2015, 6, 10, 8, 13, 12, 930000, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='subscribe',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='subscribe_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 8, 13, 20, 537000, tzinfo=utc), verbose_name=b'date subscribed'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='targetlatitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='targetlongitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='targetprice',
            field=models.FloatField(default=0.0),
        ),
    ]
