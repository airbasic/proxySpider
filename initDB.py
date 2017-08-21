#!/usr/bin/python
#coding: utf-8

from mysql import database
from config import DB_NAME

database = database()
cur = database.cur()


print "Opened database %s successfully" % DB_NAME


cur.query('''CREATE TABLE proxys
	(id INTEGER PRIMARY KEY  AUTO_INCREMENT,
	 ip CHAR(20)  NOT NULL,
	 port CHAR(10)  NOT NULL,
	 type INT  NOT NULL,
	 protocol CHAR(20) NOT NULL
	);''')

print "Table created ok"
