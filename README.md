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
4. 支持WEBSSH（websocket）
5. 文件上传至跳板机（文件上传的类型可自行修改。默认为：.xlsx,.zip,.xls,.tar,.pub,.txt）
6. 对用户用户权限进行分组.
7. 添加菜单功能
8. 记录用户操作日志
# 模块介绍
#### 后端模块：
flask、flask-mail、Flask-Script、Flask-Migrate、Flask-SQLAlchemy、SQLAlchemy、paramiko
