#!/usr/bin/python
#coding: utf-8
'''



'''
import BaseHTTPServer
import logging
import threading
import schedule
import time
import sys
import signal
from server import webReqHandler
from fetcher import proxyFetcher
from monitor import proxyMonitor
from config import API_PORT


logging.basicConfig(level=logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.CRITICAL)
logger = logging.getLogger("SPIDER")

class proxyServer():
	def __init__(self):
		self.forceExit = False

	def startFetcher(self):
		logger.info("Start Fetcher")
		fetch = proxyFetcher()
		fetch.run()
		schedule.every(40).minutes.do(fetch.run)
		while not self.forceExit:
			schedule.run_pending()
			time.sleep(1)

	def startServer(self):
		logger.info("Start Server @ %s:%s" % ('0.0.0.0',API_PORT))
		server = BaseHTTPServer.HTTPServer(('0.0.0.0',API_PORT),webReqHandler)
		server.serve_forever()

	def startMonitor(self):
		logger.info("Start Monitor")
		monitor = proxyMonitor()
		monitor.run()
		schedule.every(60).minutes.do(monitor.run)
		while not self.forceExit:
			schedule.run_pending()
			time.sleep(1)




if __name__ == "__main__":

	proxy = proxyServer()


	fetcher = threading.Thread(target=proxy.startFetcher)
	server = threading.Thread(target=proxy.startServer)
	monitor = threading.Thread(target=proxy.startMonitor)


	fetcher.start()
	server.start()
	monitor.start()




