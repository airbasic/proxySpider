from dictmysql import DictMySQL
from config import DB_NAME,DB_PASS,DB_USER,DB_HOST

#doc:https://ligyxy.github.io/DictMySQL/
class Database():
	def __init__(self):
		self.db = DictMySQL(
				db = DB_NAME,
				host = DB_HOST,
				user = DB_USER,
				passwd = DB_PASS
			)

	def cur(self):
		try:
			self.db.now()
		except Exception,e:
			self.db.reconnect()
		finally:
			return self.db