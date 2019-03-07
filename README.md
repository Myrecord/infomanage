# 功能介绍
本平台主要以运维自身的需求以及调用阿里云API来完成，都是日常基础需求，代码比较简单，可自行添加功能，方便维护。前端使用Materialize-UI页面风格简单，后端使用FLASk
#### 接口功能：
1. CDN刷新方式：预热、刷新、URL、DIR
2. 获取CDN7天的使用数据量
3. OSS云存储文件上传
4. 获取云主机信息、以及数据库信息，可手动同步数据
#### 本地功能：
1. 针对主机进行分组展示、统计
2. 显示请求的IP地址
3. 对主机执行增、删、改、查、分组
4. 支持WEBSSH
5. 文件上传至跳板机
6. 版本更新
7. 对用户权限进行分组.
8. 添加菜单功能
9. 记录用户操作日志
# 图形界面
![image](https://github.com/Myrecord/infomanage/blob/master/1.png)
![image](https://github.com/Myrecord/infomanage/blob/master/2.png)
![image](https://github.com/Myrecord/infomanage/blob/master/3.png)
![image](https://github.com/Myrecord/infomanage/blob/master/4.png)
![image](https://github.com/Myrecord/infomanage/blob/master/5.png)
# 安装配置
#### 一、准备环境
```
 安装python2.7版本
 
 安装依赖包 requirements.txt

 ```
#### 二、创建mysql数据库
```
CREATE DATABASE `infomanage` /*!40100 DEFAULT CHARACTER SET utf8 */;

用户和密码配置好后，修改config文件中的mysql地址。
```


#### 三、初始化数据库
```
删除migrations目录在进行初始化

python manage.py db init

python manage.py db migrate

python manage.py db upgrade

倒入权限表：menus.sql
```
#### 四、配置infomanage/config.py 文件
```
以下备注信息，根据自己情况更改

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
UPLOADED_FILE_DEST = '/Users/root1/infomanage/fileloads' #服务器存储上传文件的路径
SCRIPT_LOCAL_PATH = '/Users/root1/infomanage/script' #存放脚本路径
ALIYUN_ACCESS_KEYID = ''  #阿里云keyid
ALIYUN_ACCESS_KEY_SECRET = '' #阿里云key
ALIYUN_ZONE = ['cn-hangzhou', 'cn-beijing', 'cn-shenzhen', 'cn-hongkong']   #地区
OSS_ADDRESS = ''  #oss链接地址
OSS_NAME = ''    #object name
FILE_TYPE = ['.xlsx', '.xls', '.zip', '.tar', '.pub', '.txt'] #上传文件的类型
UPDATE_SCRIPT = os.path.join(SCRIPT_LOCAL_PATH,'weixin.py')  #传入脚本
UPDATE_SCRIPT_ARGS = ['222','3333','4444'] #脚本参数
CDN_DATATIME = '7' #CDN7天流量数据展示
WEBSSH_KEY_PATH = '/Users/root1/infomanage/key' #存在key文件目录
WEBSSH_KEY_NAME = 'id_rsa' #key文件名称
WEBSSH_SERVER_PORT = '22' #SSH端口
```
#### 五、注意事项
```
1.WEBSSH功能，需要用户注册的账户存在于服务器中，并使用key登录，将key放入到key目录中

2.版本更新，建议自行根据实际业务修改update.html页面，在config文件中提供有接口传入脚本以及参数，

  同时修改main/views.py中的updatedata路由，将请求参数写入到数据路中
  
3.关于首页CDN展示的数据，修改config中的CDN_DATATIME参数获取不同时间的流量信息

4.倒入数据库后默认的管理员账户：admin 密码:123123
```
#### 六、启动
```
manage.py runserver -h host -p port  #指定主机、端口
```
