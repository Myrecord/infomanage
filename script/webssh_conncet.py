import paramiko
from threading import Thread
import time
import select
import os

class Remote():

	def __init__(self):
		self.keypath = '/Users/root1/webdev/key'
		self.keyname = 'id_rsa'

	def ssh_connect(self,host,passwd,user,port=57678):
		key = os.path.join(os.path.join(self.keypath,user),self.keyname)
		try:
			self.connects = paramiko.SSHClient()
			self.connects.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.key_file = paramiko.RSAKey.from_private_key_file(key)
			self.connects.connect(host,port=port,username=user,password=passwd,pkey=self.key_file,timeout=10)
			self.channel = self.connects.invoke_shell(width=120, height=90)
			return self.channel
		except:
			return False



# a = Remote()
# a.ssh_connect('119.23.12.254','','duanpeng')
