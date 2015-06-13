# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_auto_20150610_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(default=0.0)),
                ('hotel', models.ForeignKey(to='wechat.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookingstep', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('roomtype', models.IntegerField(default=0)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
            ],
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='bookingstep',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='targetlatitude',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='targetlongitude',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='targetprice',
        ),
        migrations.AddField(
            model_name='order',
            name='weuser',
            field=models.ForeignKey(to='wechat.WechatUser'),
        ),
        migrations.AddField(
            model_name='bid',
            name='order',
            field=models.ForeignKey(to='wechat.Order'),
        ),
    ]
