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
4. 支持WEBSSH（平台登录的账户必须根服务器用户一样，并且使用key方式）
5. 文件上传至跳板机（文件上传的类型可自行修改。默认为：.xlsx,.zip,.xls,.tar,.pub,.txt）
6. 版本更新（根本用户指定时间，倒计时显示在页面中，可删除任务。此功能已实际的业务为主，编写脚本传递参数即可）
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

python manager.py db init

python manager.py db migrate

python manager.py db upgrade

倒入权限表：menus.sql
```
#### 四、配置infomanage/config.py 文件
```
```
