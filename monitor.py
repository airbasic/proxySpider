#!/usr/bin/python
#coding: utf-8


import sqlite3
import requests
import logging
import time
import json
import threading
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
		#应该要多线程处理
		self.test()

	def test(self):
		rows = self.cur.select(table='proxys',columns=['ip','port','type','protocol'])
		for row in rows:
			#print row
			proxy = row[0] + ":" + row[1]
			if 'HTTPS' in row[3]:
				proxies = { "http": "http://"+proxy, "https": "https://"+proxy}
			else:
				 proxies = { "http": "http://"+proxy}

			logger.info("DETECT Proxy [%s]" % json.dumps(proxies))
			try:
				requests.get("https://www.fliggy.com/", proxies=proxies,timeout=10)

			except Exception,e:
				logger.warn("Proxy %s is nolonger ok" % proxy)
				self.clean(ip=row[0],port=row[1])
				continue

		logger.info("finish")


if __name__ == '__main__':
	test = proxyMonitor()
	test.run()

