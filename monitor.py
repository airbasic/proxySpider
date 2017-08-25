#!/usr/bin/python
#coding: utf-8


import sqlite3
import logging
import time
import json
import threading
import eventlet
from eventlet.green import urllib2
from database import Database
from config import DB_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MONITOR")


class proxyMonitor():
	def __init__(self):
		database = Database()
		self.cur = database.cur()

	def clean(self,ip,port):
		self.cur.delete(table='proxys',where={'ip':ip,'port':port})

	def run(self):
		self.test()

	def proxyTest(self,row):
		proxy = row[0] + ":" + row[1]
		if 'HTTPS' in row[3]:
			proxies = { "https": "https://"+proxy}
		else:
			proxies = { "http": "http://"+proxy}
		ip = row[0]
		port = row[1]

		theProxy = urllib2.ProxyHandler(proxies)
		opener = urllib2.build_opener(theProxy)
		urllib2.install_opener(opener)
		testResult = 'ok!'
		try:
			webcode = urllib2.urlopen("https://www.fliggy.com/",timeout=10).getcode()
			#logger.info("Proxy %s is ok" % proxy)
		except Exception,e:
			#logger.warn("Proxy %s is nolonger ok" % proxy)
			self.clean(ip=ip,port=port)
			testResult = 'nolonger ok!'
		finally:
			return proxy, testResult

	def test(self):
		rows = self.cur.select(table='proxys',columns=['ip','port','type','protocol'])
		pool = eventlet.GreenPool(300)
		for proxies,testResult in pool.imap(self.proxyTest,rows):
			logger.info("DETECT Proxy [%s] Finished,it is %s" % (proxies,testResult))
		logger.info("Monitor Process finish")


if __name__ == '__main__':
	test = proxyMonitor()
	test.run()

