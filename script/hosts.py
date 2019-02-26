import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import pickle


class hostinfo():

	def __init__(self):
		self.zone = ['cn-hangzhou', 'cn-beijing', 'cn-shenzhen', 'cn-hongkong', ]
		self.info = []
		self.page = 4
		self.count = {}

	def get_host(self):
		for zone in self.zone:
			self.client = AcsClient('', '', zone) #阿里云key
			for page_number in range(1, self.page):
				request = DescribeInstancesRequest.DescribeInstancesRequest()
				request.set_accept_format('json')
				request.set_PageNumber(page_number)
				request.set_PageSize('100')
				result = json.loads(self.client.do_action_with_exception(request))
				self.info.append(result['Instances']['Instance'])
		return self.info

	def grouping_count(self):
		self.get_host()
		for zone in self.zone:
			for zone_host in sum(self.info,[]):
				if zone == zone_host['RegionId']:
				    self.count.setdefault(zone,[]).append(zone_host['RegionId'])
		print self.count
		for key,values in self.count.items():
			self.count[key] = len(values)
		with open('grouping_host_count','w') as files:
			pickle.dump(self.count,files)
