# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

#from wechat_sdk import WechatBasic
from wesimp import WechatSimple
from .models import WechatUser
from .models import Hotel
from .models import Order
from .models import Bid


import logging
import os

logger = logging.getLogger('django')

# Create your views here.
def update_user(openid, nickname=None, phone=None, subscribe_date=None, 
			sex=None, subscribe=None, latitude=None, longitude=None):
	if WechatUser.objects.filter(openid=openid).count() >= 1 :
		u = WechatUser.objects.get(openid=openid)
	else:		
		u = WechatUser(openid=openid, nickname="nick", phone="phone", sex=0)
	if nickname is not None:
		u.nickname = nickname
	if phone is not None:
		u.phone = phone
	if subscribe_date is not None:
		u.subscribe_date = subscribe_date
	if sex is not None:
		u.sex = sex
	if subscribe is not None:
		u.subscribe = subscribe
	if latitude is not None:
		u.latitude = latitude
	if longitude is not None:
		u.longitude = longitude
	u.save()

	
def get_user_all():
	all_wechat_users = WechatUser.objects.all()
	output = ', '.join([u.openid for u in all_wechat_users])
	return output

def InterfaceVerify(request):
	signature = request.GET.get('signature', None)
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	echostr = request.GET.get('echostr', None)
	wechat = WechatSimple()
	if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
		return HttpResponse(echostr)

def ProcessRequest(request):
	signature = request.GET.get('signature')
	timestamp = request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	wechat = WechatSimple()
	body_text = request.body
	if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
		wechat.parse_data(body_text)
		message = wechat.get_message()

		response = None
		if message.type == 'text':
			if message.content == u'订房':
				response = wechat.response_text(u'您好，请点击按钮订房，或者下载呼呼睡App：http://ftpqy.vicp.net/admin/')
			else:
				response = wechat.response_text(u'文字')
		elif message.type == 'image':
			response = wechat.response_text(u'图片')
		elif message.type == 'event':
			response = wechat.response_text(u'消息')
		elif message.type == 'subscribe':
			update_user(openid=message.source, subscribe_date=timezone.now(), subscribe=1)
			response = wechat.response_text(u'您好，欢迎关注呼呼睡微信服务号。您可以点击按钮订房，也可以下载呼呼睡App进行订房。')
		elif message.type == 'location':
			update_user(openid=message.source, latitude=message.latitude, longitude=message.longitude)
			response = wechat.response_text(message.type)
		else:
			response = wechat.response_text(message.type)
		
		return HttpResponse(response)

@csrf_exempt
def index(request):
	if request.method == 'GET':
		return InterfaceVerify(request)
	else:
		return ProcessRequest(request)

@csrf_exempt
def booking(request):
	#wechat = WechatSimple()
	#code = request.GET.get('code', None)
	#snsret = wechat.oauth(code)
	#openid = snsret["openid"];

	openid = 'oFlDUs4VBB_ZXGqnYOhwRkTu2clc'
	WechatUser.objects.get(openid = openid)
	orders = Order.objects.all()
	bids = Bid.objects.all()
	context = {'openid': openid, 'orders': orders, 'bids': bids}
	return render(request, 'wechat/booking.html', context)

@csrf_exempt
def test(request):
	#return creatmenu(request)
	#return getmenu(request)
	#update_user(openid="123", subscribe_date=timezone.now())
	#update_user(openid="556", subscribe_date=timezone.now(), subscribe=1)
	return HttpResponse(get_user_all())

def creatmenu(request):
	wechat = WechatSimple()
	retval = wechat.create_menu({
		'button':[
		{
			'type': 'view',
			'name': '我要订房!',
			'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx57a085415d1caaed&redirect_uri=http://ftpqy.vicp.net/wechat/booking/?action=viewtest&response_type=code&scope=snsapi_base&state=1#wechat_redirect'
		},
	]})
	return HttpResponse(json.dumps(retval))
	
def getmenu(request):
	wechat = WechatSimple()
	return HttpResponse(json.dumps(wechat.get_menu()))