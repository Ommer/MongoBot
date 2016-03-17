from pymongo import MongoClient




class RobotDatabase(object):

	def __init__(self, host, port, verbose_stream):

		self._connection = self._connect(host,port)
		

	def _connect(self, host, port):
		print "- Establishing Mongo database connection"
		client = MongoClient()
		#print dir(client)
		return client.ReportDB

	def get_collection(self,db):

		return db.reports.find()

	def get_collection_runId(self, id):
		return db.report.find({'run_id':'56e9d680f7507a7cc39000ec'})
    
