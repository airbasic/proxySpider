#coding: utf-8
import sys
#COMMON
DB_NAME = 'PROXY'
DB_USER = 'root'
DB_PASS = 'admin88888'
DB_HOST = 'localhost'
#

#FETCHER
#爬虫爬取列表
proxyUrlList = [
	{
		'title': '快代理',
		'urls': ['http://www.kuaidaili.com/proxylist/%s/'% n for n in range(1,11)],
		'pattern': '//*[@id="freelist"]/table/tbody/tr[position()>0]',
		'postion': {'ip':'./td[1]','port':'./td[2]','type':'./td[3]','protocol':'./td[4]'}
	},
	{
		'title': '西刺代理',
		'urls':['http://www.xicidaili.com/nn/%s' % n for n in range(1,2000)],
		'pattern': '//*[@id="ip_list"]/tr[position()>0]',
		'postion':{'ip':'./td[2]','port':'./td[3]','type':'./td[5]','protocol':'./td[6]'}
	}

]




#SERVER
API_PORT=8888