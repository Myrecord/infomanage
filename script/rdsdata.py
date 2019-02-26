import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkcorev3.clientv3 import AcsClient as AcsClientv3
from aliyunsdkcorev3.request import CommonRequest

class datainfo():
	def __init__(self):
		self.zone = ['cn-hangzhou','cn-shenzhen',]
		self.types = ['sharding', 'replicate']
		self.DBid = []
		self.DBinfo = []
		#self.query_mysql()
		#self.query_redis()
		#self.query_mogo()


	def get_DBid(self):
		try:
			for zone in self.zone:
				client = AcsClient('LTAIareXfGARtOV0', 'Jxu5aMNVVaX4qe5AAYEheCdqvYigzm', zone)
				request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
				request.set_accept_format('json')
				response = json.loads(client.do_action_with_exception(request))
				self.DBid.append(response['Items']['DBInstance'])
		except Exception as e:
			raise e

	def query_mysql(self):
		self.get_DBid()
		for zone in self.zone:
			client = AcsClient('LTAIareXfGARtOV0', 'Jxu5aMNVVaX4qe5AAYEheCdqvYigzm',zone)
			for ids in sum(self.DBid, []):
				request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
				request.set_accept_format('json')
				request.set_DBInstanceId(ids['DBInstanceId'])
				response = json.loads(client.do_action_with_exception(request))
				self.DBinfo.append(response['Items']['DBInstanceAttribute'])
			return self.DBinfo

	def query_redis(self):
		for zone in self.zone:
			client  = AcsClientv3('LTAIareXfGARtOV0', 'Jxu5aMNVVaX4qe5AAYEheCdqvYigzm',zone)
			request = CommonRequest()
			request.set_accept_format('json')
			request.set_domain('r-kvstore.aliyuncs.com')
			request.set_action_name('DescribeInstances')
			request.set_version('2015-01-01')
			response = json.loads(client.do_action_with_exception(request))
			self.DBinfo.append(response['Instances']['KVStoreInstance'])
		return self.DBinfo

	def query_mogo(self):
		for zone in self.zone:
			client  = AcsClientv3('LTAIareXfGARtOV0', 'Jxu5aMNVVaX4qe5AAYEheCdqvYigzm',zone)
			for types in self.types:
				request = CommonRequest()
				request.set_accept_format('json')
				request.set_domain('mongodb.aliyuncs.com')
				request.set_action_name('DescribeDBInstances')
				request.set_version('2015-12-01')
				request.add_query_param('DBInstanceType',types)
				response = json.loads(client.do_action_with_exception(request))
				self.DBinfo.append(response['DBInstances']['DBInstance'])
		return self.DBinfo



# a = datainfo()
# for i in sum(a.DBinfo,[]):
# 	print i['']