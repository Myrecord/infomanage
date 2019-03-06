# -*- coding: utf-8 -*-
import oss2
import os
import pickle
from datetime import datetime
from flask import current_app


class Ossoperation:

	def __init__(self):
		self.endpoint = current_app.config['OSS_ADDRESS']
		self.auth = oss2.Auth(current_app.config['ALIYUN_ACCESS_KEYID'], current_app.config['ALIYUN_ACCESS_KEY_SECRET'])
		self.Bucket = oss2.Bucket(self.auth, self.endpoint,current_app.config['OSS_NAME'])

	def get_fileinfo(self):
		dir_files = {}
		try:
			for i in oss2.ObjectIterator(self.Bucket):
				dirname = i.key.split('/')[0]
				filename = i.key.split('/')[1]
				if filename:
					files_size = self.Bucket.get_object_meta(os.path.join(dirname,filename)).content_length
					files_lasttime = self.Bucket.get_object_meta(os.path.join(dirname,filename)).last_modified
					dates = datetime.utcfromtimestamp(files_lasttime).strftime("%Y-%m-%d %H:%M")
					dir_files.setdefault(dirname,[]).append({filename:[files_size,dates]})
		except Exception as e:
			raise e
		with open(current_app.config['SCRIPT_LOCAL_PATH'] +'/' + 'oss_obj_info','w') as files:
			pickle.dump(dir_files,files)

	def upload_files(self,objname,localfile):
		oss2.resumable_upload(self.Bucket,objname,localfile,store=oss2.ResumableStore(root=current_app.config['UPLOADED_FILE_DEST']))


