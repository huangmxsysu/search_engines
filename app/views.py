#-*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render


def shouye(request):
	return render(request,'base.html')


def search(request):
	
	# if 'searchword' in request.GET:
	# 	message = 'You searched for: %r' % request.GET['searchword']
	# else:
	# 	message = 'You submitted an empty form.'
	print(request.GET['searchword'])
	print(type(request.GET['searchword']))

	searchword = request.GET['searchword']
	
	
	sousuolist = [ { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
				    'title': '龙岗布吉怡康家园56平米',
				    'price': 2200,
				    'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
				    'addr': '大芬村深惠公路西侧沃尔玛斜',
				    'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } ,
				    

				    { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
				    'title': '龙岗布吉怡康家园56平米',
				    'price': 2200,
				    'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
				    'addr': '大芬村深惠公路西侧沃尔玛斜',
				    'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } ,


				    { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
				    'title': '龙岗布吉怡康家园56平米',
				    'price': 2200,
				    'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
				    'addr': '大芬村深惠公路西侧沃尔玛斜',
				    'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } 
				    ]

	print(type(sousuolist))

	return render(request, 'show_result.html', {'searchword':searchword,'sousuolist': sousuolist})


	
