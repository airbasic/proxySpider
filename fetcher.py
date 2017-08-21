#!/usr/bin/python
#coding: utf-8

import sqlite3
import requests
import logging
from lxml import etree
from database import Database
from config import proxyUrlList,DB_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FETCHER")

class proxyFetcher():
	def __init__(self):
		database = Database()
		self.cur = database.cur()

	def HTMLDownloader(self,url):
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
		try:
			content = requests.get(url,headers=headers,timeout=10).text
			#print content
			#logger.info("get %s" % content)
		except Exception,e:
			logger.warn("HTML Down Failed [%s]" % str(e))
			content = '<html></html>'
		finally:
			return content


	def save(self,ip,port,proxytype,protocol):
		if not self.isProxyExsit(ip,port):
			self.cur.insert(table='proxys',value={'ip':ip,'port':port,'type':proxytype,'protocol':protocol})
			logger.debug("Store Proxy [%s:%s]" % (ip,port))
		else:
			logger.debug("Pass a exsits Proxy [%s:%s]" %(ip,port))


	def isProxyExsit(self,ip,port):
		result = self.cur.get(table='proxys',column='id',where={'ip':ip,'port':port})
		if result:
			return True
		else:
			return False

	def run(self):
		for proxyConf in proxyUrlList:
			logger.info("正在抓取 %s 的代理..." % proxyConf['title'])
			urls = proxyConf['urls']
			pattern = proxyConf['pattern']
			postion = proxyConf['postion']

			for url in urls:
				html = self.HTMLDownloader(url)
				selector = etree.HTML(html)
				proxys = selector.xpath(pattern)
				#print proxys[0].text
				for proxy in proxys:
					try:
						ip = proxy.xpath(postion['ip'])[0].text
						port = proxy.xpath(postion['port'])[0].text
						proxytype = proxy.xpath(postion['type'])[0].text
						if proxytype.find(u'高匿') != -1:
							proxytype = 1
						else:
							proxytype = 0
						protocol = proxy.xpath(postion['protocol'])[0].text
						logger.info("IP:%s,PORT:%s,TYPE:%s,PROTOCOL:%s" % (ip,port,proxytype,protocol))
						self.save(ip,port,proxytype,protocol)
					except Exception,e:
						logger.warning(str(e))
						continue
		logger.info("fetch finished")

if __name__ == "__main__":
	test = proxyFetcher()
	test.run()