import json
from datetime import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20141111 import RefreshObjectCachesRequest
from aliyunsdkcdn.request.v20141111 import PushObjectCacheRequest
from aliyunsdkcdn.request.v20141111 import DescribeRefreshQuotaRequest
from aliyunsdkcdn.request.v20141111 import DescribeRefreshTasksRequest
from aliyunsdkcdn.request.v20141111 import DescribeTopDomainsByFlowRequest


class pushcdn():
	def __init__(self):
		self.client = AcsClient('', '', 'cn-hangzhou')
		self.domain = []
		self.domain_ranking = {}


	def get_domain(self):
		try:
			request = DescribeTopDomainsByFlowRequest.DescribeTopDomainsByFlowRequest()
			request.set_accept_format('json')
			start_time = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT00:00:00Z')
			end_time = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
			request.set_StartTime(start_time)
			request.set_EndTime(end_time)
			result = json.loads(self.client.do_action_with_exception(request))
			for i in result['TopDomains']['TopDomain']:
				self.domain_ranking[i['DomainName']] = i['TotalTraffic']
			return self.domain_ranking
		except Exception as e:
			raise e

	def records(self):
		try:
			request = DescribeRefreshTasksRequest.DescribeRefreshTasksRequest()
			request.set_accept_format('json')
			request.set_PageSize('10')
			result = json.loads(self.client.do_action_with_exception(request))
			return result['Tasks']['CDNTask']
		except Exception as e:
			raise e

	def pushdomain(self, url):
		try:
			request = PushObjectCacheRequest.PushObjectCacheRequest()
			request.set_ObjectPath(url)
			result = json.loads(self.client.do_action_with_exception(request))
		except Exception as e:
			raise e

	def refredomain(self, url, types):
		try:
			request = RefreshObjectCachesRequest.RefreshObjectCachesRequest()
			if types == 'directory':
				request.set_ObjectType('Directory')
				request.set_ObjectPath(url)
				result = json.loads(self.client.do_action_with_exception(request))
			else:
				request.set_ObjectPath(url)
				result = json.loads(self.client.do_action_with_exception(request))
		except Exception as e:
			raise (e)

	def selectnumber(self):
		try:
			request = DescribeRefreshQuotaRequest.DescribeRefreshQuotaRequest()
			request.set_accept_format('json')
			result = json.loads(self.client.do_action_with_exception(request))
		except Exception as e:
			raise e
		else:
			return result
