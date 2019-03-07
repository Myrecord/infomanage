import os

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = 'Infomanage'
    FLASKY_MAIL_SENDER = 'admin@qq.com' #系统发件人
    FLASKY_ADMIN = 'admin@qq.com' #管理员邮件地址
    DEBUG = True
    MAIL_SERVER = 'smtp.exmail.qq.com' #邮件服务器
    MAIL_PORT = 465  #邮件端口
    MAIL_USE_TLS = False 
    MAIL_USE_SSL = True 
    MAIL_USERNAME = 'admin@qq.com' #邮件账户
    MAIL_PASSWORD = '123123'		#邮件密码
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/infomanage' #mysql数据库地址
    SCHEDULER_API_ENABLED = True
    use_reloader=False
    UPLOADED_FILE_DEST = '/Users/root1/infomanage/fileloads'
    SCRIPT_LOCAL_PATH = '/Users/root1/infomanage/script'
    ALIYUN_ACCESS_KEYID = ''  #阿里云keyid
    ALIYUN_ACCESS_KEY_SECRET = '' #阿里云key
    ALIYUN_ZONE = ['cn-hangzhou', 'cn-beijing', 'cn-shenzhen', 'cn-hongkong']   #地区
    OSS_ADDRESS = ''  #oss链接地址
    OSS_NAME = ''    #object name
    FILE_TYPE = ['.xlsx', '.xls', '.zip', '.tar', '.pub', '.txt']
    UPDATE_SCRIPT = os.path.join(SCRIPT_LOCAL_PATH,'weixin.py')
    UPDATE_SCRIPT_ARGS = ['222','3333','4444']
    CDN_DATATIME = '7' #CDN7天流量数据展示

    @staticmethod
    def init_app(app):
        pass

config = {'default':Config}
