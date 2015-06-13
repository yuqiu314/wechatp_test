# -*- coding: utf-8 -*-

import hashlib
import requests
import time
import json
import cgi
from StringIO import StringIO

from xml.dom import minidom

from .messages import MESSAGE_TYPES, UnknownMessage
from .exceptions import ParseError, NeedParseError, NeedParamError, OfficialAPIError
from .reply import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, Article, ArticleReply
from .lib import disable_urllib3_warning, XMLStore

import weglobal

class WechatSimple(object):
	def __init__(self, checkssl=False):
		if not checkssl:
			disable_urllib3_warning()  # 可解决 InsecurePlatformWarning 警告
		self.__is_parse = False
		self.__message = None

	def check_signature(self, signature, timestamp, nonce):
		if not signature or not timestamp or not nonce:
			return False
		tmp_list = [weglobal.TOKEN, timestamp, nonce]
		tmp_list.sort()
		tmp_str = ''.join(tmp_list)
		if signature == hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
			return True
		else:
			return False
			
	def parse_data(self, data):
		result = {}
		if type(data) == unicode:
			data = data.encode('utf-8')
		elif type(data) == str:
			pass
		else:
			raise ParseError()

		try:
			xml = XMLStore(xmlstring=data)
		except Exception:
			raise ParseError()

		result = xml.xml2dict
		result['raw'] = data
		result['type'] = result.pop('MsgType').lower()

		message_type = MESSAGE_TYPES.get(result['type'], UnknownMessage)
		self.__message = message_type(result)
		self.__is_parse = True
			
	def get_message(self):
		return self.__message

	def response_text(self, content, escape=False):
		if self.__is_parse:
			content = self._transcoding(content)
			if escape:
				content = cgi.escape(content)
			return TextReply(message=self.__message, content=content).render()
			
	def _transcoding(self, data):
		if not data:
			return data
		result = None
		if isinstance(data, str):
			result = data.decode('utf-8')
		else:
			result = data
		return result
		
	def _transcoding_list(self, data):
		if not isinstance(data, list):
			raise ValueError('Parameter data must be list object.')
		result = []
		for item in data:
			if isinstance(item, dict):
				result.append(self._transcoding_dict(item))
			elif isinstance(item, list):
				result.append(self._transcoding_list(item))
			else:
				result.append(item)
		return result
		
	def _transcoding_dict(self, data):
		if not isinstance(data, dict):
			raise ValueError('Parameter data must be dict object.')
		result = {}
		for k, v in data.items():
			k = self._transcoding(k)
			if isinstance(v, dict):
				v = self._transcoding_dict(v)
			elif isinstance(v, list):
				v = self._transcoding_list(v)
			else:
				v = self._transcoding(v)
			result.update({k: v})
		return result

	def _check_official_error(self, json_data):
		if "errcode" in json_data and json_data["errcode"] != 0:
			raise OfficialAPIError("{}: {}".format(json_data["errcode"], json_data["errmsg"]))

	def _request(self, method, url, **kwargs):
		if "params" not in kwargs:
			kwargs["params"] = {
				"access_token": self.get_accesstoken(),
			}
		if isinstance(kwargs.get("data", ""), dict):
			body = json.dumps(kwargs["data"], ensure_ascii=False)
			body = body.encode('utf8')
			kwargs["data"] = body

		r = requests.request(
			method=method,
			url=url,
			**kwargs
		)
		r.raise_for_status()
		response_json = r.json()
		self._check_official_error(response_json)
		return response_json
		
	def _get(self, url, **kwargs):
		return self._request(
			method="get",
			url=url,
			**kwargs
		)

	def _post(self, url, **kwargs):
		return self._request(
			method="post",
			url=url,
			**kwargs
		)
		
	def get_accesstoken(self):
		if not weglobal.ACCESS_TOKEN or int(time.time()) >=  weglobal.ACCESS_TOKEN_EXPIRES_AT:
			response_json = self._get(
				url="https://api.weixin.qq.com/cgi-bin/token",
				params={
					"grant_type": "client_credential",
					"appid": weglobal.APP_ID,
					"secret": weglobal.APP_SECRET,
				}
			)
			weglobal.ACCESS_TOKEN = response_json['access_token']
			weglobal.ACCESS_TOKEN_EXPIRES_AT = int(time.time()) + response_json['expires_in']
		return weglobal.ACCESS_TOKEN
		
	def create_menu(self, menu_data):
		menu_data = self._transcoding_dict(menu_data)
		return self._post(
			url='https://api.weixin.qq.com/cgi-bin/menu/create',
			data=menu_data
		)
		
	def get_menu(self):
		return self._get('https://api.weixin.qq.com/cgi-bin/menu/get')
		
	def oauth(self, code):
		#换取网页授权access_token页面的构造方式：
		#https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
		response_json = self._get(
			url="https://api.weixin.qq.com/sns/oauth2/access_token",
			params={
				"grant_type": "authorization_code",
				"appid": weglobal.APP_ID,
				"secret": weglobal.APP_SECRET,
				"code": code,
			}
		)
		return response_json