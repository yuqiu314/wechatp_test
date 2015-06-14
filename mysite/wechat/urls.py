from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^test/$', views.test, name='test'),
	url(r'^booking/$', views.booking, name='booking'),
	url(r'^hotelogin/$', views.hotelogin, name='hotelogin'),
	url(r'^hotelreg/$', views.hotelreg, name='hotelreg'),
	url(r'^hotelogout/$', views.hotelogout, name='hotelogout'),
	url(r'^ordersforhotel/$', views.ordersforhotel, name='ordersforhotel'),
]