# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Hotel(models.Model):
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	latitude = models.FloatField(default=0.000000)
	longitude = models.FloatField(default=0.000000)

class WechatUser(models.Model):
	openid = models.CharField(max_length=200)
	nickname = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	subscribe_date = models.DateTimeField('date subscribed')
	sex = models.IntegerField(default=0)
	subscribe = models.IntegerField(default=0)
	latitude = models.FloatField(default=0.000000)
	longitude = models.FloatField(default=0.000000)

class Order(models.Model):
	weuser = models.ForeignKey(WechatUser)
	bookingstep = models.IntegerField(default=0)
	price = models.FloatField(default=0.00)
	roomtype = models.IntegerField(default=0)
	latitude = models.FloatField(default=0.000000)
	longitude = models.FloatField(default=0.000000)

class Bid(models.Model):
	order = models.ForeignKey(Order)
	hotel = models.ForeignKey(Hotel)
	price = models.FloatField(default=0.00)
	
	