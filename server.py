#!/usr/bin/python
#coding: utf-8
'''


'''
import sqlite3
import BaseHTTPServer
import json
import logging
import urlparse
import urllib
from database import Database
from config import API_PORT,DB_NAME

logger = logging.getLogger("SERVER")

class webReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def paramsDict(self,path):
		pDict = {}
		parsedPath = urlparse.urlparse(path)
		try:
			query = urllib.unquote(parsedPath.query)
			if query == '':
				return pDict
			if query.find('&') != -1:
				params = query.split('&')
				for param in params:
					pDict[param.split('=')[0]] = param.split('=')[1]
			else:
				pDict[query.split('=')[0]] = query.split('=')[1]
			return pDict

		except Exception,e:
			logger.warning(str(e))
			return pDict


	def toInt(self,string):
		if string.isdigit():
			return string
		else:
			return 1

	def do_GET(self):
		pDict = self.paramsDict(self.path)
		if pDict == {}:
			self.send_response(403)
			return

		content = []
		limit = '100'
		proxytype0 = '0'
		proxytype1 = '1'
		protocol = '%HTTP%'
		for key in pDict:
			if key == 'limit':
				limit = self.toInt(pDict[key])
			if key == 'type':
				proxytype0 = self.toInt(pDict[key])
				proxytype1 = self.toInt(pDict[key])
			if key == 'protocol':
				protocol = '%'+pDict[key]+'%'


		database = Database()
		cur = database.cur()
		rows = cur.select(table='proxys',columns=['ip','port','type','protocol'],where={'$AND':[{'$OR':[{'type':proxytype0},{'type':proxytype1}]},{'$LIKE':{'protocol':protocol}}]},limit=limit)
		for row in rows:
			ip = row[0]
			port = row[1]
			proxytype = row[2]
			protocol = row [3]
			content.append({"ip":ip,"port":port,"type":proxytype,"protocol":protocol})

		content = json.dumps(content,indent=1)

		self.send_response(200)
		self.end_headers()
		self.wfile.write(content)
