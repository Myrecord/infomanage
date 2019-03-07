import os

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = 'Infomanage'
    FLASKY_MAIL_SENDER = 'admin@qq.com'
    FLASKY_ADMIN = 'admin@qq.com'
    DEBUG = True
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False 
    MAIL_USE_SSL = True 
    MAIL_USERNAME = 'admin@qq.com'
    MAIL_PASSWORD = '123123'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/infomanage'
    SCHEDULER_API_ENABLED = True
    use_reloader=False
    UPLOADED_FILE_DEST = '/Users/root1/infomanage/fileloads'
    SCRIPT_LOCAL_PATH = '/Users/root1/infomanage/script'
    ALIYUN_ACCESS_KEYID = ''
    ALIYUN_ACCESS_KEY_SECRET = ''
    ALIYUN_ZONE = ['cn-hangzhou', 'cn-beijing', 'cn-shenzhen', 'cn-hongkong']
    OSS_ADDRESS = ''
    OSS_NAME = ''
    FILE_TYPE = ['.xlsx', '.xls', '.zip', '.tar', '.pub', '.txt']
    UPDATE_SCRIPT = os.path.join(SCRIPT_LOCAL_PATH,'weixin.py')
    UPDATE_SCRIPT_ARGS = ['222','3333','4444']
    CDN_DATATIME = '7'
    WEBSSH_KEY_PATH = '/Users/root1/webdev/key'
    WEBSSH_KEY_NAME = 'id_rsa'
    WEBSSH_SERVER_PORT = '57678'

    @staticmethod
    def init_app(app):
        pass

config = {'default':Config}
