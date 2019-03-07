import paramiko
import os
from flask import current_app


class Remote():

	def __init__(self):
		self.keypath = current_app.config['WEBSSH_KEY_PATH']
		self.keyname = current_app.config['WEBSSH_KEY_NAME']
		self.port = current_app.config['WEBSSH_SERVER_PORT']

	def ssh_connect(self,host,passwd,user):
		key = os.path.join(os.path.join(self.keypath,user),self.keyname)
		try:
			self.connects = paramiko.SSHClient()
			self.connects.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.key_file = paramiko.RSAKey.from_private_key_file(key)
			self.connects.connect(host,port=self.port,username=user,password=passwd,pkey=self.key_file,timeout=10)
			self.channel = self.connects.invoke_shell(width=120, height=90)
			return self.channel
		except:
			return False


